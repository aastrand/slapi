# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import re

from lxml import objectify

TYPES = set(['Buses', 'Metros', 'Trains', 'Trams'])


METRO_VALUES = ('TransportMode', 'GroupOfLine', 'StationName', 'LineNumber',
                'Destination')
METRO_DISPLAY = ('DisplayRow1', 'DisplayRow2')
TRAIN_DISPLAY = 'DisplayTime'

DISPLAY_NAME_RE = re.compile('^([0-9]+) +([a-zA-ZåäöÅÄÖ\.]+) ([0-9]+[:0-9]* ?[min]*\.?) ?,?')

ENCODING = 'UTF-8'


def parse_displayrow(text):
    data = []
    # each line can contain more than one line/destination/time tuple
    # iterate over each match, extract, remove matched data and try again
    while len(text) > 0:
        match = DISPLAY_NAME_RE.match(text)
        if match:
            row = {}
            row['linenumber'] = match.group(1)
            row['destination'] = match.group(2)
            row['displaytime'] = match.group(3).strip()
            data.append(row)
            text = text[len(match.group(0)):].strip()
        else:
            logging.debug('Display row mismatch: %s' % text)
            break
    return data


def get_now():
    return datetime.datetime.now()


def convert_time(time):
    if ':' in time:
        now = get_now()

        hour, minute = time.split(':')
        dtime = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                  hour=int(hour), minute=int(minute))

        # 00.00 wraparound?
        if dtime < now:
            dtime = dtime + datetime.timedelta(days=1)

        time = round((dtime - now).total_seconds() / 60.0)

    elif 'min' in time:
        time = time.replace('min', '').replace('.', '').strip()

    return int(time)


def parse_xml_response(text):
    xml = objectify.fromstring(text.encode(ENCODING))
    data = []
    # iterate over buses, trains, trams etc
    for transport_type in xml.iterchildren():
        # strip namespace when checking for tagnames
        if transport_type.tag[transport_type.tag.rfind('}')+1:] in TYPES:
            # Metros/Metro sub iteration
            for item in transport_type.iterchildren():
                row = {}
                for value in METRO_VALUES:
                    if hasattr(item, value):
                        row[value.lower()] = item[value].text.encode(ENCODING)

                # split up metro displayrows into individual elements
                if hasattr(item, METRO_DISPLAY[0]):
                    for value in METRO_DISPLAY:
                        for display_row in parse_displayrow(item[value].text.encode(ENCODING)):
                            row = copy.deepcopy(row)
                            row.update(display_row)
                            data.append(row)
                # else (trains etc), extract time as normal
                elif hasattr(item, TRAIN_DISPLAY):
                    row['displaytime'] = item[TRAIN_DISPLAY].text.encode(ENCODING)
                    data.append(row)

    # sort on time to departure
    for element in data:
        element['time'] = convert_time(element['displaytime'])
    data.sort(key=lambda x: x['time'])

    return data


# TODO:
def get_departures(station):
    pass
