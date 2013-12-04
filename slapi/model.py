# -*- coding: utf-8 -*-

import copy
import datetime
import json
import logging
import re

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
TRAIN_URL_TEMPLATE = 'https://api.trafiklab.se/sl/realtid/GetDpsDepartures.json?&siteId=%s&key=%s'

# i dont care about fjärrtåg
BANNED_DESTINATIONS = set([u'Fjärrtåg'])


class ApiException(Exception):
    pass


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


def parse_json_response(text):
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
    jdata = json.loads(text)
    data = []
    # iterate over buses, trains, trams etc
    for transport_type, transport in jdata.get('Departure', jdata.get('DPS', {})).iteritems():
        # Metros/Metro sub iteration
        if transport_type in TYPES and transport:
            for item in transport.values()[0]:
                row = {}
                for value in METRO_VALUES:
                    if value in item:
                        row[value.lower()] = item[value]

                # split up metro displayrows into individual elements,
                # since they are encoded in the actual displayrows
                # that you see when waiting at the station
                # this includes warnings about pickpockets and other nonsense
                if METRO_DISPLAY[0] in item:
                    for value in METRO_DISPLAY:
                        for display_row in parse_displayrow(item[value]):
                            row = copy.deepcopy(row)
                            row.update(display_row)
                            data.append(row)
                # else (trains etc), extract time as normal
                if TRAIN_DISPLAY in item:
                    row[u'displaytime'] = item[TRAIN_DISPLAY]
                    data.append(row)

    # convert time to minutes for sorting
    # remove banned destinations
    banned_elements = []
    for element in data:
        if element[u'destination'] in BANNED_DESTINATIONS:
            banned_elements.append(element)
        element[u'time'] = convert_time(element[u'displaytime'])

    # deferred removal to not upset iteration
    for element in banned_elements:
        data.remove(element)

    return data


def get_departure(url_template, station, key):
    """
    Helper function to get the parses response for the given
    URL, station and API key.
    """
    r = requests.get(url_template % (station, key))
    if r.status_code != 200:
        raise ApiException('Error while querying the trafiklab API')

    return parse_json_response(r.text)


def get_departures(station, key):
    """
    Returns a list of all departures for the given station.
    Each element describes a departure, encoded as a dictionary.
    The list is ordered by departure time, ascending order.
    The API key needs to be a valid trafiklab API key.
    """
    data = get_departure(METRO_URL_TEMPLATE, station, key)
    data.extend(get_departure(TRAIN_URL_TEMPLATE, station, key))

    # sort on time to departure
    data.sort(key=lambda x: x['time'])

    return data
