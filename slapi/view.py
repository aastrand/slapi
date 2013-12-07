# -*- coding: utf-8 -*-


PRE_HEADER = ['<table id="sl_time_table">']
PRE_HEADER.append('<tr><th style="width:3%"></th>')
PRE_HEADER.append('<th style="width:75px;text-align:center"><img src="https://dl.dropboxusercontent.com/u/7823835/SL/SL_logo.svg" height="30px" /></th>')
HEADER_NAME = '<th style="color:#888888;padding-left:20;font-size:24px">%s </th>'
POST_HEADER = [('<th style="color:#888888;width:12%;text-align:center;font-size:24px">min.</th>')]
POST_HEADER.append('</tr>')

PRE_ROW = '<tr>'
COLOUR_ROW = '<td style="background-color:%s"></td>'
DESCRIPTION_ROW = '<td class="projectLine" style="color:lightGray">%s</td>'
DESTINATION_ROW = '<td class="projectDestination">%s</td>'
TIME_ROW = '<td class="projectTime" style="text-align:center">%s</td>'
POST_ROW = '</tr>'

POST_ALL = '</table>'

TRANSPORT_COLOR = {u'BLUEBUS': 'blue',
                   u'BUS': 'red',
                   u'TRAM': 'mediumGray',
                   u'TRAIN': 'mediumGray'}
METRO_COLOR = {u'Tunnelbanans blå linje': 'blue',
               u'Tunnelbanans gröna linje': 'green',
               u'Tunnelbanans röda linje': 'red'}

IMAGE_TEMPLATE = '<img src="https://dl.dropboxusercontent.com/u/7823835/SL/%s" height="40px" />'
TRANSPORT_IMAGE = {u'TRAIN': IMAGE_TEMPLATE % 'J.png',
                   u'Spårväg City': IMAGE_TEMPLATE % 'S.png',
                   u'Tvärbanan': IMAGE_TEMPLATE % 'L.png',
                   u'Tunnelbanans blå linje': IMAGE_TEMPLATE % 'T-bla.png',
                   u'Tunnelbanans gröna linje': IMAGE_TEMPLATE % 'T-gron.png',
                   u'Tunnelbanans röda linje': IMAGE_TEMPLATE % 'T-rod.png'}


def get_transport_color(departure):
    """
    Lookup function for the tab colors of the given departure.
    """
    return TRANSPORT_COLOR.get(departure[u'transportmode'],
                               METRO_COLOR.get(departure.get(u'groupofline'),
                                               'mediumGray'))


def get_description(departure):
    """
    Lookup function for the description of the given departure.
    """
    description = TRANSPORT_IMAGE.get(departure[u'transportmode'],
                                      TRANSPORT_IMAGE.get(departure.get(u'groupofline')))

    if not description:
        description = departure.get(u'linenumber') or departure.get(u'groupofline')

    return description


def render_html_table(station_name, data):
    """
    Renders a html <table><tr><td></td></tr></table view
    of the given station name and departures.
    """
    output = []
    output.extend(PRE_HEADER)
    output.append(HEADER_NAME % station_name)
    output.extend(POST_HEADER)

    for departure in data:
        output.append(PRE_ROW)
        output.append(COLOUR_ROW % get_transport_color(departure))
        output.append(DESCRIPTION_ROW % get_description(departure))
        output.append(DESTINATION_ROW % departure[u'destination'])
        output.append(TIME_ROW % departure[u'time'])
        output.append(POST_ROW)

    output.append(POST_ALL)

    return '\n'.join(output)
