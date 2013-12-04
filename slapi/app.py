# -*- coding: utf-8 -*-

import json
import logging

from flask import Flask, request, make_response

from model import get_departures, ApiException

app = Flask(__name__)
app.debug = True
log = logging.getLogger()


def get_args(args):
    """
    Helper function to extract the mandatory (*) and optional (-)
    arguments to this web API:
    * key      - trafiklab API key
    - distance - distance to the station in minutes, will filter out
                 departures that will be missed
    - limit    - limit the amount of departures in the response
    """
    key = args.get('key')
    if key is None:
        raise ValueError('Missing mandatory argument: key')

    distance = get_int_argument(request.args, 'distance', 0)
    limit = get_int_argument(request.args, 'limit', None)

    return key, distance, limit


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


# TODO: create view.py
def render(data):
    return str(data)


@app.route("/<int:station>")
def sl(station):
    """
    Entry point for the API.
    Takes a single argument, the station resource as an integer.
    """
    # unpack arguments
    try:
        key, distance, limit = get_args(request.args)
    except ValueError, e:
        resp = make_response(str(e), 400)
        return resp

    # fetch data from model given our station
    try:
        data = get_departures(station, key)
    except ApiException, e:
        resp = make_response(str(e), 503)
        return resp

    # respect arguments
    if distance:
        data = [d for d in data if d['time'] > distance]
    if limit is not None:
        data = data[:limit]

    # render results and send response
    if request.args.get('alt') == 'json':
        resp = make_response(json.dumps(data, ensure_ascii=False).encode('UTF-8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    else:
        resp = make_response(render(data).encode('UTF-8'))
        resp.headers['Content-Type'] = 'text/html; charset=utf-8'

    return resp


if __name__ == "__main__":
    app.run()
