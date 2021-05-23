# -*- coding: utf-8 -*-

import datetime
import json
import logging

from flask import Flask, request, make_response

from model import (get_departures, get_station_name, ApiException,
                   compile_whitelist)
from view import render_html_table
from util import load_config

app = Flask(__name__)
log = logging.getLogger()
app.api_config = load_config('/config.yaml')


def get_args(args):
    """
    Helper function to extract the mandatory (*) and optional (-)
    arguments to this web API:
    - distance - distance to the station in minutes, will filter out
                 departures that will be missed
    - limit    - limit the amount of departures in the response

    Optional whitelist arguments as comma separated lists of lines:
    - buses
    - metros
    - trains
    - trams

    """
    distance = get_int_argument(request.args, 'distance', 0)
    limit = get_int_argument(request.args, 'limit', None)
    whitelist = compile_whitelist(request.args)

    return distance, limit, whitelist


def get_int_argument(args, argname, default=0):
    """
    Helper function to extract an integer argument.
    Will raise ValueError if the argument exists but is not an integer.
    Will return the default if the argument is not found.
    """
    arg = args.get(argname)
    if arg is not None:
        try:
            arg = int(arg)
        except ValueError:
            raise ValueError('Error while parsing argument %s' % argname)
    else:
        arg = default

    return arg


def json_default(obj):
    """
    Default handler for the json dumping.
    Sometimes the departures contain datetimes.
    """
    if isinstance(obj, datetime.datetime):
        return str(obj)


@app.route("/v1/station/<int:station>/departures")
def departures(station):
    """
    Returns the departures for the given station.
    """
    # unpack arguments
    try:
        distance, limit, whitelist = get_args(request.args)
    except ValueError as e:
        log.exception(str(e))
        resp = make_response(str(e), 400)
        return resp

    # fetch data from model given our station
    try:
        data = get_departures(station, app.api_config['departure-key'], whitelist)
        station_name = get_station_name(station, app.api_config['station-key'])
    except ApiException as e:
        log.exception(str(e))
        resp = make_response(str(e), 503)
        return resp

    # respect arguments
    if distance:
        data = [d for d in data if d['time'] > distance]
    if limit is not None:
        data = data[:limit]

    # render results and send response
    if request.args.get('alt') == 'json':
        resp = make_response(json.dumps(data, ensure_ascii=False,
                                        default=json_default).encode('UTF-8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    else:
        resp = make_response(render_html_table(station_name, data).encode('UTF-8'))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'

    return resp


@app.route("/v1/station/<int:station>")
def station(station):
    """
    Returns the name for the given station.
    """
    # fetch data from model given our station
    try:
        station_name = get_station_name(station, app.api_config['station-key'])
    except ApiException as e:
        log.exception(str(e))
        resp = make_response(str(e), 503)
        return resp

    data = {'name': station_name, 'siteid': str(station)}
    # render results and send response
    resp = make_response(json.dumps(data, ensure_ascii=False).encode('UTF-8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")
