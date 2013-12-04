# -*- coding: utf-8 -*-

import json
import unittest

import slapi.app as app
import slapi.model as model

from mock import patch, Mock
from flask import request


RENDER_EXPECTED = """<table id="sl_time_table">
<tr><th style="width:3%"></th>
<th style="width:75px;text-align:center"><img src="https://dl.dropboxusercontent.com/u/7823835/SL/SL_logo.svg" height="30px" /></th>
<th style="color:#888888;padding-left:20;font-size:24px">test </th>
<th style="color:#888888;width:12%;text-align:center;font-size:24px">min.</th>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="http://www.carlfranzon.com/wp-content/uploads/J.png" height="40px" /></td>
<td class="projectDestination">kongo</td>
<td class="projectTime" style="text-align:center">2</td>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="http://www.carlfranzon.com/wp-content/uploads/J.png" height="40px" /></td>
<td class="projectDestination">lars</td>
<td class="projectTime" style="text-align:center">3</td>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="http://www.carlfranzon.com/wp-content/uploads/J.png" height="40px" /></td>
<td class="projectDestination">jimmy</td>
<td class="projectTime" style="text-align:center">5</td>
</tr>
<tr>
<td style="background-color:mediumGray"></td>
<td class="projectLine" style="color:lightGray"><img src="http://www.carlfranzon.com/wp-content/uploads/J.png" height="40px" /></td>
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

        with app.app.test_request_context('/crap'):
            r = app.sl('crap')
            self.assertEquals(r.status_code, 400)

        with app.app.test_request_context('/9325'):
            r = app.sl(9325)
            self.assertEquals(r.response,
                              ['Missing mandatory argument: key'])

        with app.app.test_request_context('/9325?key=test123'):
            r = app.sl(9325)
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

        with app.app.test_request_context('/9325?key=test123'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            self.assertEquals(r.response, [RENDER_EXPECTED])

        # json rendering
        with app.app.test_request_context('/9325?key=test123&alt=json'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}])

        # limit
        with app.app.test_request_context('/9325?key=test123&alt=json&limit=crap'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 400)
            self.assertEquals(r.response,
                              ['Error while parsing argument limit'])

        with app.app.test_request_context('/9325?key=test123&alt=json&limit=3'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 2, 'transportmode': 'TRAIN',
                                      'destination': 'kongo'},
                                     {'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'}])

        # distance
        with app.app.test_request_context('/9325?key=test123&alt=json&distance=3'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'},
                                     {'time': 10, 'transportmode': 'TRAIN',
                                      'destination': 'jeppson'}])

        # combine
        with app.app.test_request_context('/9325?key=test123&alt=json&distance=2&limit=2'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 3, 'transportmode': 'TRAIN',
                                      'destination': 'lars'},
                                     {'time': 5, 'transportmode': 'TRAIN',
                                      'destination': 'jimmy'}])
