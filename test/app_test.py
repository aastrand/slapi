# -*- coding: utf-8 -*-

import json
import unittest

import slapi.app as app
import slapi.model as model

from mock import patch, Mock
from flask import request


class ModelTest(unittest.TestCase):

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

    @patch('slapi.app.get_departures')
    def test_args(self, get_dep_mock):
        get_dep_mock.return_value = [{'time': 2},
                                     {'time': 3},
                                     {'time': 5},
                                     {'time': 10}]

        with app.app.test_request_context('/9325?key=test123'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            # TODO: rendering
            self.assertEquals(r.response, ["[{'time': 2}, {'time': 3}, {'time': 5}, {'time': 10}]"])

        # json rendering
        with app.app.test_request_context('/9325?key=test123&alt=json'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 2},
                                     {'time': 3},
                                     {'time': 5},
                                     {'time': 10}])

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
            self.assertEquals(resp, [{'time': 2},
                                     {'time': 3},
                                     {'time': 5}])

        # distance
        with app.app.test_request_context('/9325?key=test123&alt=json&distance=3'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 5},
                                     {'time': 10}])

        # combine
        with app.app.test_request_context('/9325?key=test123&alt=json&distance=2&limit=2'):
            r = app.sl(9325)
            self.assertEquals(r.status_code, 200)
            resp = json.loads(r.response[0])
            self.assertEquals(resp, [{'time': 3},
                                     {'time': 5}])
