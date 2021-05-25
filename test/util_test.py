# -*- coding: utf-8 -*-

import tempfile
import unittest

from slapi import util


CONFIG_EXAMPLE = """
departure-key: donkey
station-key: horse
"""


class UtilTest(unittest.TestCase):

    def test_load_config(self):
        expected = {'departure-key': 'donkey',
                    'station-key': 'horse'}
        with tempfile.NamedTemporaryFile(mode='wt') as t:
            t.write(CONFIG_EXAMPLE)
            t.flush()
            c = util.load_config(t.name)
            self.assertEqual(c, expected)

        with tempfile.NamedTemporaryFile(mode='wt') as t:
            t.write('crap')
            t.flush()
            self.assertRaises(ValueError, util.load_config, t.name)

        with tempfile.NamedTemporaryFile(mode='wt') as t:
            self.assertRaises(ValueError, util.load_config, t.name)

        self.assertRaises(IOError, util.load_config, '/tmp/does/not/exist')
