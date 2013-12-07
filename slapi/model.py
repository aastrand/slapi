# -*- coding: utf-8 -*-

import copy
import datetime
import json
import logging
import re

import gocept.cache.method as cache
import requests

# we only want data for these types, errors and what not begone
TYPES = set(['Buses', 'Metros', 'Trains', 'Trams'])

# what we're interested in
METRO_VALUES = (u'TransportMode', u'GroupOfLine', u'StationName', u'LineNumber',
                u'Destination')
METRO_DISPLAY = (u'DisplayRow1', u'DisplayRow2')
TRAIN_DISPLAY = u'DisplayTime'

# combined regex for metro-style and train-style displayrows
# matches both HH:MM and MM min style times
DISPLAY_NAME_RE = re.compile('^([0-9]+) +([a-zA-ZåäöÅÄÖ\.]+) *([0-9]+[:0-9]* ?[min]*\.?) *,?')

METRO_URL_TEMPLATE = 'https://api.trafiklab.se/sl/realtid/GetDepartures.json?&siteId=%s&key=%s'
TRAIN_URL_TEMPLATE = 'https://api.trafiklab.se/sl/realtid/GetDpsDepartures.json?&siteId=%s&key=%s&timeWindow=60'
STATION_URL_TEMPLATE = 'https://api.trafiklab.se/sl/realtid/GetSite.json?&stationSearch=%s&key=%s'

# i dont care about fjärrtåg
BANNED_DESTINATIONS = set([u'Fjärrtåg'])


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
    # encode, otherwise we dont match Kungsträdgården etc
    text = text.encode('UTF-8')
    data = []
    # each line can contain more than one line/destination/time tuple
    # iterate over each match, extract, remove matched data and try again
    while len(text) > 0:
        match = DISPLAY_NAME_RE.match(text)
        if match:
            row = {}
            row[u'linenumber'] = match.group(1).decode('UTF-8')
            row[u'destination'] = match.group(2).decode('UTF-8')
            row[u'displaytime'] = match.group(3).strip().decode('UTF-8')
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

    '8 min.'' => 8
    '12:22' (at the time of 12:18) => 4
    '9' => 9
    """
    if ':' in time:
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

    elif 'min' in time:
        time = time.replace('min', '').replace('.', '').strip()

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
    for transport_type, transport in jdata.get(u'Departure', jdata.get(u'DPS', {})).iteritems():
        # Metros/Metro sub iteration
        if transport_type in TYPES and transport:
            items = transport.values()[0]
            # sometimes lone items are just a dict
            if type(items) == dict:
                items = [items]

            for item in items:
                row = {}
                for value in METRO_VALUES:
                    if value in item:
                        row[value.lower()] = item[value]

                rows = []
                # split up metro displayrows into individual elements,
                # since they are encoded in the actual displayrows
                # that you see when waiting at the station
                # this includes warnings about pickpockets and other nonsense
                if METRO_DISPLAY[0] in item:
                    for value in METRO_DISPLAY:
                        for display_row in parse_displayrow(item[value]):
                            row = copy.deepcopy(row)
                            row.update(display_row)
                            rows.append(row)
                # else (trains etc), extract time as normal
                if TRAIN_DISPLAY in item:
                    row[u'displaytime'] = item[TRAIN_DISPLAY]
                    rows.append(row)

                # filter and convert time to minutes
                for row in rows:
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
    for site_type, site in jdata.get(u'Hafas', {}).iteritems():
        if site_type == u'Sites':
            for item in site.values():
                data.append({u'name': item['Name']})
    return data


def get_departure(url_template, station, key, whitelist=None):
    """
    Helper function to get the parsed response for the given
    URL, station and API key.
    """
    r = requests.get(url_template % (station, key))
    if r.status_code != 200:
        raise ApiException('Error while querying the trafiklab API')

    return parse_json_response(r.text, whitelist)


@cache.Memoize(10)
def get_departures(station, key, whitelist=None):
    """
    Returns a list of all departures for the given station.
    Each element describes a departure, encoded as a dictionary.
    The list is ordered by departure time, ascending order.
    The API key needs to be a valid trafiklab API key.
    """
    data = get_departure(METRO_URL_TEMPLATE, station, key, whitelist)
    data.extend(get_departure(TRAIN_URL_TEMPLATE, station, key, whitelist))

    # sort on time to departure
    data.sort(key=lambda x: x['time'])

    return data


@cache.Memoize(24 * 60 * 60)
def get_station_name(station, key):
    """
    Returns the name of the given station ID.
    """
    r = requests.get(STATION_URL_TEMPLATE % (station, key))
    if r.status_code != 200:
        raise ApiException('Error while querying the trafiklab API')

    data = parse_json_site_response(r.text)
    if len(data) < 1:
        raise ApiException('Site name response from trafiklab was empty')

    return data[0][u'name']
