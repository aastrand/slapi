# -*- coding: utf-8 -*-

import datetime
import json
import unittest

import slapi.app as app
import slapi.model as model

from mock import patch, Mock
from flask import request


app.app.api_config = {}
app.app.api_config['station-key'] = 'test-station-key'
app.app.api_config['departure-key'] = 'test-departure-key'


RENDER_EXPECTED = """<table id="sl_time_table">
<tr><th style="width:3%"></th>
<th style="width:75px;text-align:center"><img src="/static/SL_logo.svg" height="30px" /></th>
<th style="color:#888888;padding-left:20;font-size:24px">test </th>
<th style="color:#888888;width:12%;text-align:center;font-size:24px">min.</th>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="/static/J.png" height="40px" /></td>
<td class="projectDestination">kongo</td>
<td class="projectTime" style="text-align:center">2</td>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="/static/J.png" height="40px" /></td>
<td class="projectDestination">lars</td>
<td class="projectTime" style="text-align:center">3</td>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="/static/J.png" height="40px" /></td>
<td class="projectDestination">jimmy</td>
<td class="projectTime" style="text-align:center">5</td>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="/static/J.png" height="40px" /></td>
<td class="projectDestination">jeppson</td>
<td class="projectTime" style="text-align:center">10</td>
</tr>
</table>"""


class ModelTest(unittest.TestCase):

    @patch('slapi.app.get_station_name', Mock())
    @patch('slapi.app.get_departures')
    def test_basic_routing(self, get_dep_mock):
        def raiseit(*args):
            raise model.ApiException('crap')
        get_dep_mock.side_effect = raiseit

        with app.app.test_request_context('/v1/station/9325/departures'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 503)

    @patch('slapi.app.get_station_name', lambda *x: 'test')
    @patch('slapi.app.get_departures')
    def test_args(self, get_dep_mock):
        get_dep_mock.return_value = [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}]

        with app.app.test_request_context('/v1/station/9325/departures?'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            self.assertEquals(r.response, [RENDER_EXPECTED])

        # json rendering
        with app.app.test_request_context('/v1/station/9325/departures?alt=json'):
            get_dep_mock.return_value[3]['crap'] = datetime.datetime(2013, 01,
                                                                     01, 00,
                                                                     00, 00)
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson',
                                      'crap': u'2013-01-01 00:00:00'}])
            del get_dep_mock.return_value[3]['crap']

        # limit
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&limit=crap'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 400)
            self.assertEquals(r.response,
                              ['Error while parsing argument limit'])

        with app.app.test_request_context('/v1/station/9325/departures?alt=json&limit=3'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'}])

        # distance
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&distance=3'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}])

        # combine
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&distance=2&limit=2'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'}])

    @patch('slapi.app.get_station_name', lambda *x: 'test')
    @patch('slapi.app.get_departures')
    def test_args_whitelist(self, get_dep_mock):
        get_dep_mock.return_value = {}

        # remove buses and trams
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&buses=none&trams=none'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            expected =  {'Trams': set([u'none']), 'Buses': set([u'none'])}
            self.assertEquals(get_dep_mock.call_args_list[0][0][2], expected)
            get_dep_mock.reset_mock()

        # filter metros
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&metros=10,19'):
            r = app.departures(9325)
            self.assertEquals(r.status_code, 200)
            expected =  {'Metros': set(['10', '19'])}
            self.assertEquals(get_dep_mock.call_args_list[0][0][2], expected)
            get_dep_mock.reset_mock()

    @patch('slapi.app.get_station_name')
    def test_station(self, get_station_mock):
        get_station_mock.return_value = 'test'
        with app.app.test_request_context('/v1/station/9325'):
            r = app.station(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, {u'siteid': '9325', u'name': 'test'})

        def raiseit(*args):
            raise model.ApiException('crap')
        get_station_mock.side_effect = raiseit

        with app.app.test_request_context('/v1/station/9325?'):
            r = app.station(9325)
            self.assertEquals(r.status_code, 503)
