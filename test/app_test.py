# -*- coding: utf-8 -*-

import datetime
import json
import unittest

import slapi.main as app

from mock import patch


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

    @patch('slapi.main.get_station_name', lambda *x: 'test')
    @patch('slapi.main.get_departures')
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
            self.assertEqual(r.status_code, 200)
            self.assertEqual(str(r.response[0], 'UTF-8'), RENDER_EXPECTED)

    @patch('slapi.main.get_station_name', lambda *x: 'test')
    @patch('slapi.main.get_departures')
    def test_args_json(self, get_dep_mock):
        get_dep_mock.return_value = [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}]

        # json rendering
        with app.app.test_request_context('/v1/station/9325/departures?alt=json'):
            get_dep_mock.return_value[3]['crap'] = datetime.datetime(2013, 1,
                                                                     1, 00,
                                                                     00, 00)
            r = app.departures(9325)
            self.assertEqual(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEqual(resp, [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson',
                                      'crap': u'2013-01-01 00:00:00'}])
            del get_dep_mock.return_value[3]['crap']

    @patch('slapi.main.get_station_name', lambda *x: 'test')
    @patch('slapi.main.get_departures')
    def test_args_limit(self, get_dep_mock):
        get_dep_mock.return_value = [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}]

        # limit
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&limit=crap'):
            r = app.departures(9325)
            self.assertEqual(r.status_code, 400)
            self.assertEqual(str(r.response[0], 'UTF-8'),
                              'Error while parsing argument limit')

        with app.app.test_request_context('/v1/station/9325/departures?alt=json&limit=3'):
            r = app.departures(9325)
            self.assertEqual(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEqual(resp, [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'}])

    @patch('slapi.main.get_station_name', lambda *x: 'test')
    @patch('slapi.main.get_departures')
    def test_args_distance(self, get_dep_mock):
        get_dep_mock.return_value = [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}]
        # distance
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&distance=3'):
            r = app.departures(9325)
            self.assertEqual(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEqual(resp, [{'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}])

    @patch('slapi.main.get_station_name', lambda *x: 'test')
    @patch('slapi.main.get_departures')
    def test_args_combine(self, get_dep_mock):
        get_dep_mock.return_value = [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}]
        # combine
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&distance=2&limit=2'):
            r = app.departures(9325)
            self.assertEqual(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEqual(resp, [{'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'}])

    @patch('slapi.main.get_station_name', lambda *x: 'test')
    @patch('slapi.main.get_departures')
    def test_args_whitelist(self, get_dep_mock):
        get_dep_mock.return_value = {}

        # remove buses and trams
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&buses=none&trams=none'):
            r = app.departures(9325)
            self.assertEqual(r.status_code, 200)
            expected = {'Trams': set([u'none']), 'Buses': set([u'none'])}
            self.assertEqual(get_dep_mock.call_args_list[0][0][2], expected)
            get_dep_mock.reset_mock()

        # filter metros
        with app.app.test_request_context('/v1/station/9325/departures?alt=json&metros=10,19'):
            r = app.departures(9325)
            self.assertEqual(r.status_code, 200)
            expected = {'Metros': set(['10', '19'])}
            self.assertEqual(get_dep_mock.call_args_list[0][0][2], expected)
            get_dep_mock.reset_mock()

    @patch('slapi.main.get_station_name')
    def test_station(self, get_station_mock):
        get_station_mock.return_value = 'test'
        with app.app.test_request_context('/v1/station/9325'):
            r = app.station(9325)
            self.assertEqual(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEqual(resp, {u'siteid': '9325', u'name': 'test'})
