# -*- coding: utf-8 -*-

import json
import logging

from flask import Flask, request, make_response

from model import parse_json_response

app = Flask(__name__)
app.debug = True
log = logging.getLogger()


METRO_URL_TEMPLATE = 'https://api.trafiklab.se/sl/realtid/GetDepartures.json?&siteId=%s&key=%s'


def get_args(args):
    dist = args.get('dist', 0)
    key = args.get('key')
    if key is None:
        raise ValueError('Missing mandatory argument: key')

    return dist, key


@app.route("/<int:station>")
def sl(station):
    try:
        dist, key = get_args(request.args)
    except ValueError, e:
        resp = make_response(str(e), 400)
        return resp

    r = requests.get(METRO_URL_TEMPLATE % (station, key))
    if r.status_code != 200:
        resp = make_response('Error while querying the trafiklab API', 503)
        return resp

    data = parse_json_response(r.text)

    if request.args.get('alt') == 'json':
        resp = make_response(json.dumps(data))
        r.headers['Content-Type'] = 'application/json'
    else:
        resp = make_response(str(data))

    return resp


if __name__ == "__main__":
    app.run()
