# -*- coding: utf-8 -*-

import unittest

from slapi import view


class ViewTest(unittest.TestCase):
    def test_get_transport_color(self):
        departure = {u'destination': u'Kungsträdg.',
                     u'displaytime': u'5 min',
                     u'groupofline': u'tunnelbanans blå linje',
                     u'linenumber': u'10',
                     u'stationname': u'Sundbybergs centrum',
                     u'time': 5,
                     u'transportmode': u'METRO'}
        self.assertEqual(view.get_transport_color(departure), 'blue')

        departure[u'groupofline'] = u'tunnelbanans gröna linje'
        self.assertEqual(view.get_transport_color(departure), 'green')

        departure[u'groupofline'] = u'tunnelbanans röda linje'
        self.assertEqual(view.get_transport_color(departure), 'red')

        departure[u'groupofline'] = u'tunnelbanans gula linje'
        self.assertEqual(view.get_transport_color(departure), 'mediumGray')

        del departure[u'groupofline']
        departure[u'transportmode'] = 'BLUEBUS'
        self.assertEqual(view.get_transport_color(departure), 'blue')

        departure[u'transportmode'] = 'BUS'
        self.assertEqual(view.get_transport_color(departure), 'red')

        departure[u'transportmode'] = 'TRAM'
        self.assertEqual(view.get_transport_color(departure), 'mediumGray')

        departure[u'transportmode'] = 'TRAIN'
        self.assertEqual(view.get_transport_color(departure), 'mediumGray')

        departure[u'transportmode'] = 'DONKEY'
        self.assertEqual(view.get_transport_color(departure), 'mediumGray')

    def test_get_description(self):
        departure = {u'destination': u'Kungsträdg.',
                     u'displaytime': u'5 min',
                     u'groupofline': u'tunnelbanans blå linje',
                     u'linenumber': u'10',
                     u'stationname': u'Sundbybergs centrum',
                     u'time': 5,
                     u'transportmode': u'METRO'}

        expected = '<img src="/static/T-bla.png" height="40px" />'
        self.assertEqual(view.get_description(departure), expected)

        departure[u'groupofline'] = u'tunnelbanans gröna linje'
        expected = '<img src="/static/T-gron.png" height="40px" />'
        self.assertEqual(view.get_description(departure), expected)

        departure[u'groupofline'] = u'tunnelbanans röda linje'
        expected = '<img src="/static/T-rod.png" height="40px" />'
        self.assertEqual(view.get_description(departure), expected)

        del departure[u'groupofline']
        departure[u'transportmode'] = 'BLUEBUS'
        expected = '10'
        self.assertEqual(view.get_description(departure), expected)

    def test_render(self):
        data = [{u'destination': u'Kungsträdg.',
                 u'displaytime': u'5 min',
                 u'groupofline': u'tunnelbanans blå linje',
                 u'linenumber': u'10',
                 u'stationname': u'Sundbybergs centrum',
                 u'time': 5,
                 u'transportmode': u'METRO'},
                {u'destination': u'Kungsträdg.',
                 u'displaytime': u'5 min',
                 u'groupofline': u'tunnelbanans blå linje',
                 u'linenumber': u'10',
                 u'stationname': u'Sundbybergs centrum',
                 u'time': 5,
                 u'transportmode': u'METRO'}]
        expected = u"""<table id="sl_time_table">
<tr><th style="width:3%"></th>
<th style="width:75px;text-align:center"><img src="/static/SL_logo.svg" height="30px" /></th>
<th style="color:#888888;padding-left:20;font-size:24px">Sundbyberg </th>
<th style="color:#888888;width:12%;text-align:center;font-size:24px">min.</th>
</tr>
<tr>
<td style="background-color:blue"></td>
<td class="projectLine" style="color:lightGray"><img src="/static/T-bla.png" height="40px" /></td>
<td class="projectDestination">Kungsträdg.</td>
<td class="projectTime" style="text-align:center">5</td>
</tr>
<tr>
<td style="background-color:blue"></td>
<td class="projectLine" style="color:lightGray"><img src="/static/T-bla.png" height="40px" /></td>
<td class="projectDestination">Kungsträdg.</td>
<td class="projectTime" style="text-align:center">5</td>
</tr>
</table>"""
        self.assertEqual(view.render_html_table('Sundbyberg', data),
                         expected)
