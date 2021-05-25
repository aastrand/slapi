# -*- coding: utf-8 -*-

import datetime
import json
import logging
import re
import threading
import time

import gocept.cache.method as cache
import requests

log = logging.getLogger()

# we only want data for these types, errors and what not begone
TYPES = set(['Buses', 'Metros', 'Trains', 'Trams'])

# what we're interested in
VALUES_OF_INTEREST = (u'TransportMode',
                      u'StationName',
                      u'LineNumber',
                      u'Destination',
                      u'DisplayTime',
                      u'GroupOfLine')

# combined regex for metro-style and train-style displayrows
# matches both HH:MM and MM min style times
DISPLAY_NAME_RE = re.compile(
    r'^([0-9]+) +([a-zA-ZåäöÅÄÖ\.]+) *([0-9]+[:0-9]* ?[min]*\.?) *,?')

DEPARTURE_URL_TEMPLATE = 'http://api.sl.se/api2/realtimedeparturesV4.json?key=%s&siteid=%s&timewindow=60'
STATION_URL_TEMPLATE = 'https://api.sl.se/api2/typeahead.json?key=%s&searchstring=%s&stationsonly=true&maxresults=1'

# i dont care about fjärrtåg
BANNED_DESTINATIONS = set([u'Fjärrtåg'])


cached_data = {}


def reap_cache():
    """
    Cache eviction loop.
    Will delete stale data and hopes to prevent memory leaks.
    """
    while True:
        time.sleep(60)
        now = get_now()
        count = 0
        for station, (timestamp, data) in cached_data.items():
            if timestamp - now > datetime.timedelta(minutes=15):
                count += 1
                del cached_data[station]
        log.info('Reaper evicted %d entries from cache' % count)


reaper = threading.Thread(target=reap_cache)
reaper.daemon = True
reaper.start()


class ApiException(Exception):
    pass


def compile_whitelist(args):
    """
    Helper function to compile a whitelist from the argument dict.
    The whitelist maps transport_type => set([lines]):
    {'Trams': set(['10', '20'])}
    """
    whitelist = {}
    for t in TYPES:
        if t.lower() in args:
            whitelist[t] = set(args[t.lower()].split(','))
    return whitelist


def parse_displayrow(text):
    """
    Helper function to parse the text of the actual SL displays.
    Examples:

    10 Hjulsta 8 min. => {u'linenumber': '10',
                         'u'destination': 'Hjulsta',
                          u'displaytime': '8 min.'}

    """
    # sometimes displayrows are empty dicts
    if isinstance(text, dict):
        return []
    data = []
    # each line can contain more than one line/destination/time tuple
    # iterate over each match, extract, remove matched data and try again
    while len(text) > 0:
        match = DISPLAY_NAME_RE.match(text)
        if match:
            row = {}
            row[u'linenumber'] = match.group(1)
            row[u'destination'] = match.group(2)
            row[u'displaytime'] = match.group(3).strip()
            data.append(row)
            text = text[len(match.group(0)):].strip()
        else:
            logging.debug('Display row mismatch: %s' % text)
            break

    return data


def get_now():
    """
    Helper function to get the date as of "now"
    """
    return datetime.datetime.now()


def convert_time(time):
    """
    Helper function to convert the displaytime strings to
    an actual integer minute represenation.
    Examples:

    'Nu' => 0
    '8 min.'' => 8
    '12:22' (at the time of 12:18) => 4
    '9' => 9
    '-' => 0
    """
    if 'min' in time:
        time = time.replace('min', '').replace('.', '').strip()
    elif 'Nu' in time:
        time = 0
    elif ':' in time:
        now = get_now()
        # floor below minute
        now = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                hour=now.hour, minute=now.minute, second=0,
                                microsecond=0)

        hour, minute = time.split(':')
        dtime = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                  hour=int(hour), minute=int(minute), second=0,
                                  microsecond=0)

        # 00.00 wraparound?
        if dtime < now:
            dtime = dtime + datetime.timedelta(days=1)

        time = round((dtime - now).total_seconds() / 60.0)

    if time == '-':
        time = 0

    return int(time)


def parse_json_response(text, whitelist=None):
    """
    Parses the JSON response from trafiklab and returns
    a normalized list of departures as dictioneries.
    Each dictionary contains fields for each departure.
    The order of the list is undefined.
    Note that the time field is an integer and in minutes.

    Example outout:
    [{ u'destination': u'Kungsträdg.',
                      u'displaytime': u'5 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 5,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Kungsträdg.',
                      u'displaytime': u'5 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 5}]
    """
    if whitelist is None:
        whitelist = {}

    jdata = json.loads(text)
    data = []
    # iterate over buses, trains, trams etc
    for transport_type, transport in jdata.get(u'ResponseData', {}).items():
        # Metros/Metro sub iteration
        if transport_type in TYPES and transport:
            for item in transport:
                row = {}
                for value in VALUES_OF_INTEREST:
                    if value in item:
                        row[value.lower()] = item[value]

                # if we have a whitelist, skip if not in it
                if transport_type in whitelist and \
                   row[u'linenumber'] not in whitelist[transport_type]:
                    continue

                # filter out banned destinations
                if row[u'destination'] in BANNED_DESTINATIONS:
                    continue

                row[u'time'] = convert_time(row[u'displaytime'])
                data.append(row)

    return data


def parse_json_site_response(text):
    """
    Helper function to parse and extract the station name from the
    trafiklab JSON site response.
    """
    jdata = json.loads(text)
    data = []
    for site in jdata.get(u'ResponseData', {}):
        if site.get(u'Type') == 'Station':
            data.append({u'name': site['Name']})
    return data


@cache.Memoize(60)
def query_trafiklab(url):
    """
    Helper function for querying the trafiklab HTTP APIs.
    """
    r = requests.get(url)
    if r.status_code != 200:
        raise ApiException('Error while querying the trafiklab API')
    return r.text


def get_departure(url_template, station, key, whitelist=None):
    """
    Helper function to get the parsed response for the given
    URL, station and departure API key.
    """
    resp = query_trafiklab(url_template % (key, station))
    return parse_json_response(resp, whitelist)


def handle_flapping_displays(station, data, cached_data):
    """
    Function for finding out which (if any) of the cached departures
    should actually be in the current data list, but are hidden
    since their displayrows flapped with warnings about pickpockets.
    """
    timestamp, old_data = cached_data.get(station, (None, None))
    keep = []

    def calc_dt(ts):
        return int(round((get_now() - ts).total_seconds() / 60.0))

    if timestamp is not None:
        # convert and round the time diff to minute integer
        dt = calc_dt(timestamp)
        for old_d in old_data:
            # if the departure has already left, lets not care
            if old_d[u'transportmode'] == u'METRO' and old_d[u'time'] > dt:
                # calculate deltatime more or less accurately?
                # lists are expected to be very short, (2-4 elements)
                # so it's ok to O(n^2) here
                # find the cached departure in the new list:
                for d in data:
                    # we have the departure in our new list, dont do anything
                    # allow +/- 1 minute difference since we'll accumulate
                    # errors in the delta calc
                    if d[u'destination'] == old_d[u'destination'] and \
                       d[u'linenumber'] == old_d[u'linenumber'] and \
                       -2 < d[u'time'] + dt - old_d[u'time'] < 2:
                        break
                else:
                    # hey, we used to have this and now we dont
                    if u'firstseen' not in old_d:
                        old_d[u'firstseen'] = timestamp
                        old_d[u'firsttime'] = old_d[u'time']

                    old_d[u'time'] = old_d[u'firsttime'] - \
                        calc_dt(old_d[u'firstseen'])
                    keep.append(old_d)
    return keep


def get_departures(station, key, whitelist=None):
    """
    Returns a list of all departures for the given station.
    Each element describes a departure, encoded as a dictionary.
    The list is ordered by departure time, ascending order.
    The API key needs to be a valid trafiklab departure API key.
    """
    data = get_departure(DEPARTURE_URL_TEMPLATE, station, key, whitelist)

    # see if we have cached older entries which are still relevant
    data.extend(handle_flapping_displays(station, data, cached_data))

    # sort on time to departure
    data.sort(key=lambda x: x['time'])

    cached_data[station] = (get_now(), data)

    return data


@cache.Memoize(24 * 60 * 60)
def get_station_name(station, key):
    """
    Returns the name of the given station ID.
    The API key needs to be a valid trafiklab platsuppslagnings API key.
    """
    resp = query_trafiklab(STATION_URL_TEMPLATE % (key, station))
    data = parse_json_site_response(resp)
    if len(data) < 1:
        raise ApiException('Site name response from trafiklab was empty')

    return data[0][u'name']
