# -*- coding: utf-8 -*-

import datetime
import unittest

from mock import patch, Mock

from slapi import model


METRO_JSON_TESTINPUT = u"""
{
  "Departure": {
    "xmlnsxsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xmlnsxsd": "http://www.w3.org/2001/XMLSchema",
    "xmlns": "http://www1.sl.se/realtidws/",
    "LatestUpdate": "2013-12-04T14:43:22.0004323+01:00",
    "ExecutionTime": "00:00:00",
    "Buses": {
    },
    "Metros": {
      "Metro": [
        {
          "SiteId": "9325",
          "TransportMode": "METRO",
          "StationName": "Sundbybergs centrum",
          "GroupOfLine": "Tunnelbanans blå linje",
          "DisplayRow1": "10  Kungsträdg. 5 min",
          "DisplayRow2": "10 Kungsträdg.   5 min,      10 Kungsträdg.  12 min."
        },
        {
          "SiteId": "9325",
          "TransportMode": "METRO",
          "StationName": "Sundbybergs centrum",
          "GroupOfLine": "Tunnelbanans blå linje",
          "DisplayRow1": "10  Hjulsta 1 min",
          "DisplayRow2": "10 Hjulsta   8 min,      10 Hjulsta  16 min."
        }
      ]
    },
    "Trains": {
    },
    "Trams": {
    },
    "TrainError": {
      "HasError": "true",
      "FaultCode": "Client",
      "ErrorLevel": "Error",
      "ErrorCode": "1000",
      "ErrorSource": "/realtidws/RealTimeService.asmx/GetDepartures",
      "ErrorMessage": "Connection string is missing"
    },
    "TramError": {
      "HasError": "true",
      "FaultCode": "Client",
      "ErrorLevel": "Error",
      "ErrorCode": "1000",
      "ErrorSource": "/realtidws/RealTimeService.asmx/GetDepartures",
      "ErrorMessage": "Connection string is missing"
    }
  }
}
"""

TRAIN_JSON_TESTINPUT = u"""
{
  "DPS": {
    "xmlnsxsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xmlnsxsd": "http://www.w3.org/2001/XMLSchema",
    "xmlns": "http://www1.sl.se/realtidws/",
    "LatestUpdate": "2013-12-04T15:04:05.8238628+01:00",
    "ExecutionTime": "00:00:00.2968636",
    "Buses": {
      "DpsBus": [
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "515",
          "Destination": "Odenplan",
          "TimeTabledDateTime": "2013-12-04T15:10:00",
          "ExpectedDateTime": "2013-12-04T15:10:03",
          "DisplayTime": "5 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "504",
          "Destination": "Stora Ursvik",
          "TimeTabledDateTime": "2013-12-04T15:11:00",
          "ExpectedDateTime": "2013-12-04T15:11:00",
          "DisplayTime": "6 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Karolinska sjukhuset",
          "TimeTabledDateTime": "2013-12-04T15:14:00",
          "ExpectedDateTime": "2013-12-04T15:14:20",
          "DisplayTime": "10 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Hallonbergen",
          "TimeTabledDateTime": "2013-12-04T15:16:00",
          "ExpectedDateTime": "2013-12-04T15:18:29",
          "DisplayTime": "14 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "515",
          "Destination": "Odenplan",
          "TimeTabledDateTime": "2013-12-04T15:20:00",
          "ExpectedDateTime": "2013-12-04T15:20:00",
          "DisplayTime": "15 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Hallonbergen",
          "TimeTabledDateTime": "2013-12-04T15:26:00",
          "ExpectedDateTime": "2013-12-04T15:26:00",
          "DisplayTime": "21 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "504",
          "Destination": "Stora Ursvik",
          "TimeTabledDateTime": "2013-12-04T15:26:00",
          "ExpectedDateTime": "2013-12-04T15:26:00",
          "DisplayTime": "21 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Karolinska sjukhuset",
          "TimeTabledDateTime": "2013-12-04T15:30:00",
          "ExpectedDateTime": "2013-12-04T15:30:00",
          "DisplayTime": "25 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "515",
          "Destination": "Odenplan",
          "TimeTabledDateTime": "2013-12-04T15:30:00",
          "ExpectedDateTime": "2013-12-04T15:30:00",
          "DisplayTime": "15:30"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Hallonbergen",
          "TimeTabledDateTime": "2013-12-04T15:36:00",
          "ExpectedDateTime": "2013-12-04T15:36:00",
          "DisplayTime": "15:36"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "515",
          "Destination": "Odenplan",
          "TimeTabledDateTime": "2013-12-04T15:40:00",
          "ExpectedDateTime": "2013-12-04T15:40:00",
          "DisplayTime": "15:40"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "504",
          "Destination": "Stora Ursvik",
          "TimeTabledDateTime": "2013-12-04T15:41:00",
          "ExpectedDateTime": "2013-12-04T15:41:00",
          "DisplayTime": "15:41"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Hallonbergen",
          "TimeTabledDateTime": "2013-12-04T15:47:00",
          "ExpectedDateTime": "2013-12-04T15:47:00",
          "DisplayTime": "15:47"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Karolinska sjukhuset",
          "TimeTabledDateTime": "2013-12-04T15:45:00",
          "ExpectedDateTime": "2013-12-04T15:47:29",
          "DisplayTime": "15:45"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "515",
          "Destination": "Odenplan",
          "TimeTabledDateTime": "2013-12-04T15:50:00",
          "ExpectedDateTime": "2013-12-04T15:50:00",
          "DisplayTime": "15:50"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Karolinska sjukhuset",
          "TimeTabledDateTime": "2013-12-04T15:55:00",
          "ExpectedDateTime": "2013-12-04T15:55:00",
          "DisplayTime": "15:55"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "504",
          "Destination": "Stora Ursvik",
          "TimeTabledDateTime": "2013-12-04T15:56:00",
          "ExpectedDateTime": "2013-12-04T15:56:00",
          "DisplayTime": "15:56"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "506",
          "Destination": "Hallonbergen",
          "TimeTabledDateTime": "2013-12-04T15:58:00",
          "ExpectedDateTime": "2013-12-04T15:58:00",
          "DisplayTime": "15:58"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "12346",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs station",
          "LineNumber": "515",
          "Destination": "Odenplan",
          "TimeTabledDateTime": "2013-12-04T16:00:00",
          "ExpectedDateTime": "2013-12-04T16:00:00",
          "DisplayTime": "16:00"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Brommaplan",
          "TimeTabledDateTime": "2013-12-04T15:01:00",
          "ExpectedDateTime": "2013-12-04T15:05:43",
          "DisplayTime": "1 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Blackebergs gård",
          "TimeTabledDateTime": "2013-12-04T14:57:48",
          "ExpectedDateTime": "2013-12-04T15:09:32",
          "DisplayTime": "5 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Bromma flygplats",
          "TimeTabledDateTime": "2013-12-04T15:12:48",
          "ExpectedDateTime": "2013-12-04T15:11:34",
          "DisplayTime": "7 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Danderyds sjukhus",
          "TimeTabledDateTime": "2013-12-04T15:12:30",
          "ExpectedDateTime": "2013-12-04T15:12:26",
          "DisplayTime": "8 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Blackebergs gård",
          "TimeTabledDateTime": "2013-12-04T15:12:48",
          "ExpectedDateTime": "2013-12-04T15:12:48",
          "DisplayTime": "15:12"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Liljeholmen",
          "TimeTabledDateTime": "2013-12-04T15:14:00",
          "ExpectedDateTime": "2013-12-04T15:14:00",
          "DisplayTime": "15:14"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:16:18",
          "ExpectedDateTime": "2013-12-04T15:17:08",
          "DisplayTime": "13 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Brommaplan",
          "TimeTabledDateTime": "2013-12-04T15:12:54",
          "ExpectedDateTime": "2013-12-04T15:24:47",
          "DisplayTime": "20 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Brommaplan",
          "TimeTabledDateTime": "2013-12-04T15:22:54",
          "ExpectedDateTime": "2013-12-04T15:25:05",
          "DisplayTime": "21 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Blackebergs gård",
          "TimeTabledDateTime": "2013-12-04T15:27:48",
          "ExpectedDateTime": "2013-12-04T15:27:48",
          "DisplayTime": "23 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Danderyds sjukhus",
          "TimeTabledDateTime": "2013-12-04T15:24:30",
          "ExpectedDateTime": "2013-12-04T15:28:20",
          "DisplayTime": "24 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Liljeholmen",
          "TimeTabledDateTime": "2013-12-04T15:29:00",
          "ExpectedDateTime": "2013-12-04T15:29:00",
          "DisplayTime": "24 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Bromma flygplats",
          "TimeTabledDateTime": "2013-12-04T15:29:54",
          "ExpectedDateTime": "2013-12-04T15:29:54",
          "DisplayTime": "25 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:31:12",
          "ExpectedDateTime": "2013-12-04T15:31:12",
          "DisplayTime": "27 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Danderyds sjukhus",
          "TimeTabledDateTime": "2013-12-04T15:35:30",
          "ExpectedDateTime": "2013-12-04T15:35:30",
          "DisplayTime": "15:35"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Brommaplan",
          "TimeTabledDateTime": "2013-12-04T15:33:54",
          "ExpectedDateTime": "2013-12-04T15:35:58",
          "DisplayTime": "31 min"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Blackebergs gård",
          "TimeTabledDateTime": "2013-12-04T15:37:48",
          "ExpectedDateTime": "2013-12-04T15:37:48",
          "DisplayTime": "15:37"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Brommaplan",
          "TimeTabledDateTime": "2013-12-04T15:43:54",
          "ExpectedDateTime": "2013-12-04T15:43:54",
          "DisplayTime": "15:43"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Liljeholmen",
          "TimeTabledDateTime": "2013-12-04T15:44:00",
          "ExpectedDateTime": "2013-12-04T15:44:00",
          "DisplayTime": "15:44"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Bromma flygplats",
          "TimeTabledDateTime": "2013-12-04T15:44:54",
          "ExpectedDateTime": "2013-12-04T15:44:54",
          "DisplayTime": "15:44"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Danderyds sjukhus",
          "TimeTabledDateTime": "2013-12-04T15:45:30",
          "ExpectedDateTime": "2013-12-04T15:45:30",
          "DisplayTime": "15:45"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Blackebergs gård",
          "TimeTabledDateTime": "2013-12-04T15:47:48",
          "ExpectedDateTime": "2013-12-04T15:47:48",
          "DisplayTime": "15:47"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:46:12",
          "ExpectedDateTime": "2013-12-04T15:52:26",
          "DisplayTime": "15:46"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Brommaplan",
          "TimeTabledDateTime": "2013-12-04T15:54:54",
          "ExpectedDateTime": "2013-12-04T15:54:54",
          "DisplayTime": "15:54"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "509",
          "Destination": "Danderyds sjukhus",
          "TimeTabledDateTime": "2013-12-04T15:55:30",
          "ExpectedDateTime": "2013-12-04T15:55:30",
          "DisplayTime": "15:55"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Blackebergs gård",
          "TimeTabledDateTime": "2013-12-04T15:57:48",
          "ExpectedDateTime": "2013-12-04T15:57:48",
          "DisplayTime": "15:57"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Liljeholmen",
          "TimeTabledDateTime": "2013-12-04T15:59:00",
          "ExpectedDateTime": "2013-12-04T15:59:00",
          "DisplayTime": "15:59"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "152",
          "Destination": "Bromma flygplats",
          "TimeTabledDateTime": "2013-12-04T15:59:54",
          "ExpectedDateTime": "2013-12-04T15:59:54",
          "DisplayTime": "15:59"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "50242",
          "TransportMode": "BUS",
          "StopAreaName": "Sundbybergs torg",
          "LineNumber": "113",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T16:01:12",
          "ExpectedDateTime": "2013-12-04T16:01:12",
          "DisplayTime": "16:01"
        }
      ]
    },
    "Metros": {
    },
    "Trains": {
      "DpsTrain": [
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Bålsta",
          "TimeTabledDateTime": "2013-12-04T15:06:00",
          "ExpectedDateTime": "2013-12-04T15:06:00",
          "DisplayTime": "1 min",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Kungsängen",
          "TimeTabledDateTime": "2013-12-04T15:21:00",
          "ExpectedDateTime": "2013-12-04T15:21:00",
          "DisplayTime": "16 min",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "9002",
          "Destination": "Fjärrtåg",
          "TimeTabledDateTime": "2013-12-04T15:32:00",
          "ExpectedDateTime": "2013-12-04T15:32:00",
          "DisplayTime": "15:32",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Bålsta",
          "TimeTabledDateTime": "2013-12-04T15:36:00",
          "ExpectedDateTime": "2013-12-04T15:36:00",
          "DisplayTime": "15:36",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Kungsängen",
          "TimeTabledDateTime": "2013-12-04T15:51:00",
          "ExpectedDateTime": "2013-12-04T15:51:00",
          "DisplayTime": "15:51",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Jakobsberg",
          "TimeTabledDateTime": "2013-12-04T15:58:00",
          "ExpectedDateTime": "2013-12-04T15:58:00",
          "DisplayTime": "15:58",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "9002",
          "Destination": "Fjärrtåg",
          "TimeTabledDateTime": "2013-12-04T16:02:00",
          "ExpectedDateTime": "2013-12-04T16:02:00",
          "DisplayTime": "16:02",
          "JourneyDirection": "2"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Västerhaninge",
          "TimeTabledDateTime": "2013-12-04T15:09:00",
          "ExpectedDateTime": "2013-12-04T15:09:00",
          "DisplayTime": "4 min",
          "JourneyDirection": "1"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Nynäshamn",
          "TimeTabledDateTime": "2013-12-04T15:24:00",
          "ExpectedDateTime": "2013-12-04T15:24:00",
          "DisplayTime": "19 min",
          "JourneyDirection": "1"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Västerhaninge",
          "TimeTabledDateTime": "2013-12-04T15:39:00",
          "ExpectedDateTime": "2013-12-04T15:39:00",
          "DisplayTime": "15:39",
          "JourneyDirection": "1"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "9001",
          "Destination": "Fjärrtåg",
          "TimeTabledDateTime": "2013-12-04T15:42:00",
          "ExpectedDateTime": "2013-12-04T15:42:00",
          "DisplayTime": "15:42",
          "JourneyDirection": "1"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Västerhaninge",
          "TimeTabledDateTime": "2013-12-04T15:54:00",
          "ExpectedDateTime": "2013-12-04T15:54:00",
          "DisplayTime": "15:54",
          "JourneyDirection": "1"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAIN",
          "StopAreaName": "Sundbyberg",
          "LineNumber": "35",
          "Destination": "Nynäshamn",
          "TimeTabledDateTime": "2013-12-04T16:02:00",
          "ExpectedDateTime": "2013-12-04T16:02:00",
          "DisplayTime": "16:02",
          "JourneyDirection": "1"
        }
      ]
    },
    "Trams": {
      "DpsTram": [
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:10:00",
          "ExpectedDateTime": "2013-12-04T15:10:00",
          "DisplayTime": "15:10",
          "JourneyDirection": "1",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:25:00",
          "ExpectedDateTime": "2013-12-04T15:25:00",
          "DisplayTime": "15:25",
          "JourneyDirection": "1",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:40:00",
          "ExpectedDateTime": "2013-12-04T15:40:00",
          "DisplayTime": "15:40",
          "JourneyDirection": "1",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Solna centrum",
          "TimeTabledDateTime": "2013-12-04T15:55:00",
          "ExpectedDateTime": "2013-12-04T15:55:00",
          "DisplayTime": "15:55",
          "JourneyDirection": "1",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Alvik",
          "TimeTabledDateTime": "2013-12-04T15:10:00",
          "ExpectedDateTime": "2013-12-04T15:10:00",
          "DisplayTime": "15:10",
          "JourneyDirection": "2",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Alvik",
          "TimeTabledDateTime": "2013-12-04T15:25:00",
          "ExpectedDateTime": "2013-12-04T15:25:00",
          "DisplayTime": "15:25",
          "JourneyDirection": "2",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Alvik",
          "TimeTabledDateTime": "2013-12-04T15:40:00",
          "ExpectedDateTime": "2013-12-04T15:40:00",
          "DisplayTime": "15:40",
          "JourneyDirection": "2",
          "GroupOfLine": "Tvärbanan"
        },
        {
          "SiteId": "9325",
          "StopAreaNumber": "0",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "LineNumber": "22",
          "Destination": "Alvik",
          "TimeTabledDateTime": "2013-12-04T15:55:00",
          "ExpectedDateTime": "2013-12-04T15:55:00",
          "DisplayTime": "15:55",
          "JourneyDirection": "2",
          "GroupOfLine": "Tvärbanan"
        }
      ]
    }
  }
}
"""

SITE_JSON_TEST_INPUT = u"""
{
  "Hafas": {
    "xmlnsxsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xmlnsxsd": "http://www.w3.org/2001/XMLSchema",
    "xmlns": "http://www1.sl.se/realtidws/",
    "ExecutionTime": "00:00:00.0781270",
    "Sites": {
      "Site": {
        "Number": "5119",
        "Name": "Solna Business Park (Solna)"
      }
    }
  }
}
"""

TRAIN_JSON_ITERATION = u"""
{
    "DPS": {
        "Buses": {
            "DpsBus": [
                {
                    "Destination": "Odenplan",
                    "DisplayTime": "05:00",
                    "ExpectedDateTime": "2013-12-07T05:00:00",
                    "LineNumber": "515",
                    "SiteId": "9325",
                    "StopAreaName": "Sundbybergs station",
                    "StopAreaNumber": "12346",
                    "TimeTabledDateTime": "2013-12-07T05:00:00",
                    "TransportMode": "BUS"
                },
                {
                    "Destination": "Odenplan",
                    "DisplayTime": "05:30",
                    "ExpectedDateTime": "2013-12-07T05:30:00",
                    "LineNumber": "515",
                    "SiteId": "9325",
                    "StopAreaName": "Sundbybergs station",
                    "StopAreaNumber": "12346",
                    "TimeTabledDateTime": "2013-12-07T05:30:00",
                    "TransportMode": "BUS"
                }
            ]
        },
        "ExecutionTime": "00:00:00.2968731",
        "LatestUpdate": "2013-12-07T04:41:24.5604979+01:00",
        "Metros": {},
        "Trains": {
            "DpsTrain": {
                "Destination": "B\u00e5lsta",
                "DisplayTime": "05:36",
                "ExpectedDateTime": "2013-12-07T05:36:00",
                "JourneyDirection": "2",
                "LineNumber": "35",
                "SiteId": "9325",
                "StopAreaName": "Sundbyberg",
                "StopAreaNumber": "0",
                "TimeTabledDateTime": "2013-12-07T05:36:00",
                "TransportMode": "TRAIN"
            }
        },
        "Trams": {
            "DpsTram": {
                "Destination": "Solna centrum",
                "DisplayTime": "05:39",
                "ExpectedDateTime": "2013-12-07T05:39:00",
                "GroupOfLine": "Tv\u00e4rbanan",
                "JourneyDirection": "1",
                "LineNumber": "22",
                "SiteId": "9325",
                "StopAreaName": "Sundbybergs centrum",
                "StopAreaNumber": "0",
                "TimeTabledDateTime": "2013-12-07T05:39:00",
                "TransportMode": "TRAM"
            }
        },
        "xmlns": "http://www1.sl.se/realtidws/",
        "xmlnsxsd": "http://www.w3.org/2001/XMLSchema",
        "xmlnsxsi": "http://www.w3.org/2001/XMLSchema-instance"
    }
}
"""


import pprint


class MyPrettyPrinter(pprint.PrettyPrinter):
    """
    Pretty printer subclass used for debugging parsing input.
    Avoids some unicode shanigans.
    """
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return ("u'%s'" % object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


@patch('slapi.model.cache.Memoize', Mock())
class ModelTest(unittest.TestCase):
    def test_compile_whitelist(self):
        expected = {'Buses': set(['518', '119']),
                    'Trains': set(['11', '10', '12'])}
        self.assertEquals(model.compile_whitelist({'trains': '10,11,12',
                                                   'buses': '119,518'}),
                          expected)

        expected = {'Buses': set(['518', '119']),
                    'Trains': set(['11', '10', '12']),
                    'Trams': set(['grisar'])}
        self.assertEquals(model.compile_whitelist({'trains': '10,11,12',
                                                   'buses': '119,518',
                                                   'crap': 'johnny',
                                                   'trams': 'grisar'}),
                          expected)

    def test_parse_displayrow(self):
        expected = [{u'destination': u'Hjulsta', u'displaytime': u'11 min', u'linenumber': u'10'},
                    {u'destination': u'Hjulsta', u'displaytime': u'21 min.', u'linenumber': u'10'}]
        self.assertEquals(model.parse_displayrow(u'10 Hjulsta 11 min, 10 Hjulsta 21 min.'),
                          expected)
        expected = [{u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'14 min.'}]
        self.assertEquals(model.parse_displayrow(u'10 Kungsträdg. 14 min.'),
                          expected)

        expected = [{u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'1 min'}]
        self.assertEquals(model.parse_displayrow(u'10 Kungsträdg. 1 min'),
                          expected)

        expected = [{u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'1 min'}]
        self.assertEquals(model.parse_displayrow(u'10  Kungsträdg. 1 min'),
                          expected)

        expected = []
        self.assertEquals(model.parse_displayrow(u'Korta tåg, vänligen gå mot mitten av plattformen. Short trains, please continue to the middle of the platform.'),
                          expected)

        expected = [{u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'01:49'},
                    {u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'02:19'}]
        self.assertEquals(model.parse_displayrow(u'10 Kungsträdg. 01:49 10 Kungsträdg. 02:19'),
                          expected)

        expected = [{u'destination': u'Hjulsta', u'displaytime': u'8 min', u'linenumber': u'10'},
                    {u'destination': u'Hjulsta', u'displaytime': u'16 min.', u'linenumber': u'10'}]
        self.assertEquals(model.parse_displayrow(u'10 Hjulsta   8 min,      10 Hjulsta  16 min.'),
                          expected)

        self.assertEquals(model.parse_displayrow({}), [])

    @patch('slapi.model.get_now')
    def test_parse_response(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 00, 30)
        expected = [{ u'destination': u'Kungsträdg.',
                      u'displaytime': u'5 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 5,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Kungsträdg.',
                      u'displaytime': u'5 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 5,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Kungsträdg.',
                      u'displaytime': u'12 min.',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 12,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Hjulsta',
                      u'displaytime': u'1 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 1,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Hjulsta',
                      u'displaytime': u'8 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 8,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Hjulsta',
                      u'displaytime': u'16 min.',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'stationname': u'Sundbybergs centrum',
                      u'time': 16,
                      u'transportmode': u'METRO'}]
        expected.sort(key=lambda x: x['time'])
        out = model.parse_json_response(METRO_JSON_TESTINPUT)
        out.sort(key=lambda x: x['time'])
        self.assertEquals(out, expected)

    @patch('slapi.model.get_now')
    def test_parse_train_response(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 11, 30)
        expected = [{ u'destination': u'Odenplan',
                      u'displaytime': u'5 min',
                      u'linenumber': u'515',
                      u'time': 5,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Stora Ursvik',
                      u'displaytime': u'6 min',
                      u'linenumber': u'504',
                      u'time': 6,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'10 min',
                      u'linenumber': u'506',
                      u'time': 10,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'14 min',
                      u'linenumber': u'506',
                      u'time': 14,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'15 min',
                      u'linenumber': u'515',
                      u'time': 15,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'21 min',
                      u'linenumber': u'506',
                      u'time': 21,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Stora Ursvik',
                      u'displaytime': u'21 min',
                      u'linenumber': u'504',
                      u'time': 21,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'25 min',
                      u'linenumber': u'506',
                      u'time': 25,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'15:30',
                      u'linenumber': u'515',
                      u'time': 240,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'15:36',
                      u'linenumber': u'506',
                      u'time': 246,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'15:40',
                      u'linenumber': u'515',
                      u'time': 250,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Stora Ursvik',
                      u'displaytime': u'15:41',
                      u'linenumber': u'504',
                      u'time': 251,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'15:47',
                      u'linenumber': u'506',
                      u'time': 257,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'15:45',
                      u'linenumber': u'506',
                      u'time': 255,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'15:50',
                      u'linenumber': u'515',
                      u'time': 260,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'15:55',
                      u'linenumber': u'506',
                      u'time': 265,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Stora Ursvik',
                      u'displaytime': u'15:56',
                      u'linenumber': u'504',
                      u'time': 266,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'15:58',
                      u'linenumber': u'506',
                      u'time': 268,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'16:00',
                      u'linenumber': u'515',
                      u'time': 270,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'1 min',
                      u'linenumber': u'509',
                      u'time': 1,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'5 min',
                      u'linenumber': u'113',
                      u'time': 5,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bromma flygplats',
                      u'displaytime': u'7 min',
                      u'linenumber': u'152',
                      u'time': 7,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'8 min',
                      u'linenumber': u'509',
                      u'time': 8,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'15:12',
                      u'linenumber': u'113',
                      u'time': 222,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Liljeholmen',
                      u'displaytime': u'15:14',
                      u'linenumber': u'152',
                      u'time': 224,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'13 min',
                      u'linenumber': u'113',
                      u'time': 13,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'20 min',
                      u'linenumber': u'509',
                      u'time': 20,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'21 min',
                      u'linenumber': u'509',
                      u'time': 21,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'23 min',
                      u'linenumber': u'113',
                      u'time': 23,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'24 min',
                      u'linenumber': u'509',
                      u'time': 24,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Liljeholmen',
                      u'displaytime': u'24 min',
                      u'linenumber': u'152',
                      u'time': 24,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bromma flygplats',
                      u'displaytime': u'25 min',
                      u'linenumber': u'152',
                      u'time': 25,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'27 min',
                      u'linenumber': u'113',
                      u'time': 27,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'15:35',
                      u'linenumber': u'509',
                      u'time': 245,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'31 min',
                      u'linenumber': u'509',
                      u'time': 31,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'15:37',
                      u'linenumber': u'113',
                      u'time': 247,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'15:43',
                      u'linenumber': u'509',
                      u'time': 253,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Liljeholmen',
                      u'displaytime': u'15:44',
                      u'linenumber': u'152',
                      u'time': 254,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bromma flygplats',
                      u'displaytime': u'15:44',
                      u'linenumber': u'152',
                      u'time': 254,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'15:45',
                      u'linenumber': u'509',
                      u'time': 255,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'15:47',
                      u'linenumber': u'113',
                      u'time': 257,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'15:46',
                      u'linenumber': u'113',
                      u'time': 256,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'15:54',
                      u'linenumber': u'509',
                      u'time': 264,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'15:55',
                      u'linenumber': u'509',
                      u'time': 265,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'15:57',
                      u'linenumber': u'113',
                      u'time': 267,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Liljeholmen',
                      u'displaytime': u'15:59',
                      u'linenumber': u'152',
                      u'time': 269,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bromma flygplats',
                      u'displaytime': u'15:59',
                      u'linenumber': u'152',
                      u'time': 269,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'16:01',
                      u'linenumber': u'113',
                      u'time': 271,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'15:10',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 220,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'15:25',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 235,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'15:40',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 250,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'15:55',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 265,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Alvik',
                      u'displaytime': u'15:10',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 220,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Alvik',
                      u'displaytime': u'15:25',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 235,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Alvik',
                      u'displaytime': u'15:40',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 250,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Alvik',
                      u'displaytime': u'15:55',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 265,
                      u'transportmode': u'TRAM'},
                     {u'destination': u'Bålsta',
                      u'displaytime': u'1 min',
                      u'linenumber': u'35',
                      u'time': 1,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Kungsängen',
                      u'displaytime': u'16 min',
                      u'linenumber': u'35',
                      u'time': 16,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Bålsta',
                      u'displaytime': u'15:36',
                      u'linenumber': u'35',
                      u'time': 246,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Kungsängen',
                      u'displaytime': u'15:51',
                      u'linenumber': u'35',
                      u'time': 261,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Jakobsberg',
                      u'displaytime': u'15:58',
                      u'linenumber': u'35',
                      u'time': 268,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'4 min',
                      u'linenumber': u'35',
                      u'time': 4,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Nynäshamn',
                      u'displaytime': u'19 min',
                      u'linenumber': u'35',
                      u'time': 19,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'15:39',
                      u'linenumber': u'35',
                      u'time': 249,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'15:54',
                      u'linenumber': u'35',
                      u'time': 264,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Nynäshamn',
                      u'displaytime': u'16:02',
                      u'linenumber': u'35',
                      u'time': 272,
                      u'transportmode': u'TRAIN'}]
        expected.sort(key=lambda x: x['time'])
        out = model.parse_json_response(TRAIN_JSON_TESTINPUT)
        out.sort(key=lambda x: x['time'])
        self.assertEquals(out, expected)

    @patch('slapi.model.get_now')
    def test_parse_response_whitelist(self, now_mock):
        expected = [{ u'destination': u'Bålsta',
                      u'displaytime': u'1 min',
                      u'linenumber': u'35',
                      u'time': 1,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'4 min',
                      u'linenumber': u'35',
                      u'time': 4,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Kungsängen',
                      u'displaytime': u'16 min',
                      u'linenumber': u'35',
                      u'time': 16,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Nynäshamn',
                      u'displaytime': u'19 min',
                      u'linenumber': u'35',
                      u'time': 19,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Bålsta',
                      u'displaytime': u'15:36',
                      u'linenumber': u'35',
                      u'time': 875,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'15:39',
                      u'linenumber': u'35',
                      u'time': 878,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Kungsängen',
                      u'displaytime': u'15:51',
                      u'linenumber': u'35',
                      u'time': 890,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'15:54',
                      u'linenumber': u'35',
                      u'time': 893,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Jakobsberg',
                      u'displaytime': u'15:58',
                      u'linenumber': u'35',
                      u'time': 897,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Nynäshamn',
                      u'displaytime': u'16:02',
                      u'linenumber': u'35',
                      u'time': 901,
                      u'transportmode': u'TRAIN'}]
        whitelist = {'Trains': set(['35']),
                     'Trams': set(['none']),
                     'Buses': set(['none'])}
        expected.sort(key=lambda x: x['time'])
        out = model.parse_json_response(TRAIN_JSON_TESTINPUT, whitelist)
        out.sort(key=lambda x: x['time'])
        self.assertEquals(out, expected)

    @patch('slapi.model.get_now')
    def test_parse_train_response_iteration(self, now_mock):
        expected = [{ u'destination': u'Odenplan',
                      u'displaytime': u'05:00',
                      u'linenumber': u'515',
                      u'time': 239,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'05:30',
                      u'linenumber': u'515',
                      u'time': 269,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bålsta',
                      u'displaytime': u'05:36',
                      u'linenumber': u'35',
                      u'time': 275,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'05:39',
                      u'groupofline': u'Tvärbanan',
                      u'linenumber': u'22',
                      u'time': 278,
                      u'transportmode': u'TRAM'}]
        expected.sort(key=lambda x: x['time'])
        out = model.parse_json_response(TRAIN_JSON_ITERATION)
        out.sort(key=lambda x: x['time'])
        self.assertEquals(out, expected)

    @patch('slapi.model.get_now')
    def test_convert_time(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 13, 02)
        self.assertEquals(model.convert_time('13:10'), 8)

        now_mock.return_value = datetime.datetime(2013, 12, 01, 23, 42)
        self.assertEquals(model.convert_time('00:15'), 33)

        now_mock.return_value = datetime.datetime(2013, 12, 01, 23, 42, 30)
        self.assertEquals(model.convert_time('23:42'), 0)

        self.assertEquals(model.convert_time('10 min'), 10)
        self.assertEquals(model.convert_time('1 min.'), 1)

        self.assertEquals(model.convert_time('100'), 100)

    @patch('slapi.model.requests')
    @patch('slapi.model.get_now')
    def test_get_departure(self, now_mock, req_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 13, 02)
        req_mock.get = Mock()
        req_mock.get.return_value = Mock()
        req_mock.get.return_value.status_code = 500

        self.assertRaises(model.ApiException, model.get_departure,
                          'http://test/%s/%s', 31337, 'deadbeef')

        req_mock.get.return_value.status_code = 200
        req_mock.get.return_value.text = METRO_JSON_TESTINPUT

        out = model.get_departure('http://test/%s/%s', 31337, 'deadbeef')
        self.assertEquals(type(out), list)
        self.assertEquals(len(out), 6)
        for item in out:
            self.assertEquals(type(item), dict)
            self.assertTrue(len(item) > 0)

    @patch('slapi.model.requests')
    @patch('slapi.model.get_now')
    def test_get_departures(self, now_mock, req_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 13, 02)
        req_mock.get = Mock()
        req_mock.get.return_value = Mock()
        req_mock.get.return_value.status_code = 500

        self.assertRaises(model.ApiException, model.get_departures,
                          31337, 'deadbeef')

        responses = [METRO_JSON_TESTINPUT, TRAIN_JSON_TESTINPUT]

        def mock_get(*args):
            resp = Mock()
            resp.status_code = 200
            resp.text = responses.pop(0)
            return resp

        req_mock.get = mock_get

        out = model.get_departures(31337, 'deadbeef')
        self.assertEquals(type(out), list)
        self.assertEquals(len(out), 72)
        for item in out:
            self.assertEquals(type(item), dict)
            self.assertTrue(len(item) > 0)

    def test_parse_site_response(self):
        expected = [{u'name': u'Solna Business Park (Solna)'}]
        self.assertEquals(model.parse_json_site_response(SITE_JSON_TEST_INPUT),
                          expected)

    @patch('slapi.model.requests')
    def test_get_station_name(self, req_mock):
        req_mock.get = Mock()
        req_mock.get.return_value = Mock()
        req_mock.get.return_value.status_code = 500

        self.assertRaises(model.ApiException, model.get_station_name,
                          31337, 'deadbeef')

        def mock_get(*args):
            resp = Mock()
            resp.status_code = 200
            resp.text = '{}'
            return resp

        req_mock.get = mock_get

        self.assertRaises(model.ApiException, model.get_station_name,
                          31337, 'deadbeef')

        responses = [SITE_JSON_TEST_INPUT]

        def mock_get(*args):
            resp = Mock()
            resp.status_code = 200
            resp.text = responses.pop(0)
            return resp

        req_mock.get = mock_get

        self.assertEquals(model.get_station_name(31337, 'deadbeef'),
                          u'Solna Business Park (Solna)')
