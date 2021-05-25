# -*- coding: utf-8 -*-

import pprint
import copy
import datetime
import unittest

from mock import patch, Mock

from slapi import model


DEPARTURE_JSON_TESTINPUT = u"""
{
  "ResponseData": {
    "StopPointDeviations": [
      {
        "Deviation": {
          "ImportanceLevel": 9,
          "Consequence": null,
          "Text": "För avgångstider, var god se sl.se eller tidtabell på hållplatsen."
        },
        "StopInfo": {
          "GroupOfLine": "Tvärbanan",
          "TransportMode": "TRAM",
          "StopAreaName": "Sundbybergs centrum",
          "StopAreaNumber": 0
        }
      }
    ],
    "Ships": [],
    "Trams": [],
    "Trains": [
      {
        "SiteId": 9325,
        "Destination": "Bålsta",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "Nu",
        "JourneyDirection": 2,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6032,
        "StopPointDesignation": "2",
        "TimeTabledDateTime": "2015-02-17T13:06:00",
        "ExpectedDateTime": "2015-02-17T13:07:07"
      },
      {
        "SiteId": 9325,
        "Destination": "Västerhaninge",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "2 min",
        "JourneyDirection": 1,
        "SecondaryDestinationName": "Stockholm C",
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6031,
        "StopPointDesignation": "3",
        "TimeTabledDateTime": "2015-02-17T13:09:00",
        "ExpectedDateTime": "2015-02-17T13:09:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Kungsängen",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "14 min",
        "JourneyDirection": 2,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6032,
        "StopPointDesignation": "2",
        "TimeTabledDateTime": "2015-02-17T13:21:00",
        "ExpectedDateTime": "2015-02-17T13:21:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Nynäshamn",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "17 min",
        "JourneyDirection": 1,
        "SecondaryDestinationName": "Stockholm C",
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6031,
        "StopPointDesignation": "3",
        "TimeTabledDateTime": "2015-02-17T13:24:00",
        "ExpectedDateTime": "2015-02-17T13:24:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Fjärrtåg",
        "LineNumber": "9002",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "13:32",
        "JourneyDirection": 2,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6032,
        "StopPointDesignation": "2",
        "TimeTabledDateTime": "2015-02-17T13:32:00",
        "ExpectedDateTime": "2015-02-17T13:32:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Bålsta",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "29 min",
        "JourneyDirection": 2,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6032,
        "StopPointDesignation": "2",
        "TimeTabledDateTime": "2015-02-17T13:36:00",
        "ExpectedDateTime": "2015-02-17T13:36:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Västerhaninge",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "13:39",
        "JourneyDirection": 1,
        "SecondaryDestinationName": "Stockholm C",
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6031,
        "StopPointDesignation": "3",
        "TimeTabledDateTime": "2015-02-17T13:39:00",
        "ExpectedDateTime": "2015-02-17T13:39:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Fjärrtåg",
        "LineNumber": "9001",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "13:42",
        "JourneyDirection": 1,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6031,
        "StopPointDesignation": "3",
        "TimeTabledDateTime": "2015-02-17T13:42:00",
        "ExpectedDateTime": "2015-02-17T13:42:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Kungsängen",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "13:51",
        "JourneyDirection": 2,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6032,
        "StopPointDesignation": "2",
        "TimeTabledDateTime": "2015-02-17T13:51:00",
        "ExpectedDateTime": "2015-02-17T13:51:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Nynäshamn",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "13:54",
        "JourneyDirection": 1,
        "SecondaryDestinationName": "Stockholm C",
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6031,
        "StopPointDesignation": "3",
        "TimeTabledDateTime": "2015-02-17T13:54:00",
        "ExpectedDateTime": "2015-02-17T13:54:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Bålsta",
        "LineNumber": "35",
        "TransportMode": "TRAIN",
        "Deviations": null,
        "DisplayTime": "14:06",
        "JourneyDirection": 2,
        "SecondaryDestinationName": null,
        "StopAreaName": "Sundbyberg",
        "StopAreaNumber": 6031,
        "StopPointNumber": 6032,
        "StopPointDesignation": "2",
        "TimeTabledDateTime": "2015-02-17T14:06:00",
        "ExpectedDateTime": "2015-02-17T14:06:00"
      }
    ],
    "Buses": [
      {
        "SiteId": 9325,
        "Destination": "Rissne",
        "LineNumber": "504",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "4 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:11:00",
        "ExpectedDateTime": "2015-02-17T13:11:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Liljeholmen",
        "LineNumber": "152",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "5 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:12:02",
        "ExpectedDateTime": "2015-02-17T13:12:02"
      },
      {
        "SiteId": 9325,
        "Destination": "Danderyds sjukhus",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "6 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:09:57",
        "ExpectedDateTime": "2015-02-17T13:12:17"
      },
      {
        "SiteId": 9325,
        "Destination": "Odenplan",
        "LineNumber": "515",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:15",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:15:00",
        "ExpectedDateTime": "2015-02-17T13:15:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Bromma flygplats",
        "LineNumber": "152",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "8 min",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:13:57",
        "ExpectedDateTime": "2015-02-17T13:15:11"
      },
      {
        "SiteId": 9325,
        "Destination": "Karolinska sjukhuset",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "9 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50304,
        "StopPointDesignation": "B",
        "TimeTabledDateTime": "2015-02-17T13:14:00",
        "ExpectedDateTime": "2015-02-17T13:15:13"
      },
      {
        "SiteId": 9325,
        "Destination": "Hallonbergen",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "9 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:16:00",
        "ExpectedDateTime": "2015-02-17T13:16:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Solna centrum",
        "LineNumber": "113",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "10 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:16:11",
        "ExpectedDateTime": "2015-02-17T13:16:22"
      },
      {
        "SiteId": 9325,
        "Destination": "Brommaplan",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "12 min",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:16:56",
        "ExpectedDateTime": "2015-02-17T13:18:49"
      },
      {
        "SiteId": 9325,
        "Destination": "Danderyds sjukhus",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:24",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:24:57",
        "ExpectedDateTime": "2015-02-17T13:24:57"
      },
      {
        "SiteId": 9325,
        "Destination": "Rissne",
        "LineNumber": "504",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "20 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:26:00",
        "ExpectedDateTime": "2015-02-17T13:26:18"
      },
      {
        "SiteId": 9325,
        "Destination": "Blackebergs gård",
        "LineNumber": "113",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:27",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:27:33",
        "ExpectedDateTime": "2015-02-17T13:27:33"
      },
      {
        "SiteId": 9325,
        "Destination": "Karolinska sjukhuset",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "22 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50304,
        "StopPointDesignation": "B",
        "TimeTabledDateTime": "2015-02-17T13:29:00",
        "ExpectedDateTime": "2015-02-17T13:29:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Odenplan",
        "LineNumber": "515",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:30",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:30:00",
        "ExpectedDateTime": "2015-02-17T13:30:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Hallonbergen",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "24 min",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:31:00",
        "ExpectedDateTime": "2015-02-17T13:31:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Brommaplan",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "29 min",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:31:56",
        "ExpectedDateTime": "2015-02-17T13:35:33"
      },
      {
        "SiteId": 9325,
        "Destination": "Danderyds sjukhus",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:39",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:39:57",
        "ExpectedDateTime": "2015-02-17T13:39:57"
      },
      {
        "SiteId": 9325,
        "Destination": "Rissne",
        "LineNumber": "504",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:41",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:41:00",
        "ExpectedDateTime": "2015-02-17T13:41:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Liljeholmen",
        "LineNumber": "152",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:42",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:42:02",
        "ExpectedDateTime": "2015-02-17T13:42:02"
      },
      {
        "SiteId": 9325,
        "Destination": "Karolinska sjukhuset",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:44",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50304,
        "StopPointDesignation": "B",
        "TimeTabledDateTime": "2015-02-17T13:44:00",
        "ExpectedDateTime": "2015-02-17T13:44:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Bromma flygplats",
        "LineNumber": "152",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:44",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:44:33",
        "ExpectedDateTime": "2015-02-17T13:44:33"
      },
      {
        "SiteId": 9325,
        "Destination": "Odenplan",
        "LineNumber": "515",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:45",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:45:00",
        "ExpectedDateTime": "2015-02-17T13:45:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Solna centrum",
        "LineNumber": "113",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:46",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:46:11",
        "ExpectedDateTime": "2015-02-17T13:46:11"
      },
      {
        "SiteId": 9325,
        "Destination": "Hallonbergen",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:46",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:46:00",
        "ExpectedDateTime": "2015-02-17T13:46:20"
      },
      {
        "SiteId": 9325,
        "Destination": "Brommaplan",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:46",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:46:56",
        "ExpectedDateTime": "2015-02-17T13:46:56"
      },
      {
        "SiteId": 9325,
        "Destination": "Danderyds sjukhus",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:54",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50242,
        "StopPointDesignation": "C",
        "TimeTabledDateTime": "2015-02-17T13:54:57",
        "ExpectedDateTime": "2015-02-17T13:54:57"
      },
      {
        "SiteId": 9325,
        "Destination": "Rissne",
        "LineNumber": "504",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:56",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T13:56:00",
        "ExpectedDateTime": "2015-02-17T13:56:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Blackebergs gård",
        "LineNumber": "113",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:57",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T13:57:33",
        "ExpectedDateTime": "2015-02-17T13:57:33"
      },
      {
        "SiteId": 9325,
        "Destination": "Karolinska sjukhuset",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "13:59",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50304,
        "StopPointDesignation": "B",
        "TimeTabledDateTime": "2015-02-17T13:59:00",
        "ExpectedDateTime": "2015-02-17T13:59:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Odenplan",
        "LineNumber": "515",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "14:00",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T14:00:00",
        "ExpectedDateTime": "2015-02-17T14:00:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Hallonbergen",
        "LineNumber": "506",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "14:01",
        "JourneyDirection": 1,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs station",
        "StopAreaNumber": 12346,
        "StopPointNumber": 50439,
        "StopPointDesignation": "A",
        "TimeTabledDateTime": "2015-02-17T14:01:00",
        "ExpectedDateTime": "2015-02-17T14:01:00"
      },
      {
        "SiteId": 9325,
        "Destination": "Brommaplan",
        "LineNumber": "509",
        "TransportMode": "BUS",
        "Deviations": null,
        "DisplayTime": "14:01",
        "JourneyDirection": 2,
        "GroupOfLine": null,
        "StopAreaName": "Sundbybergs torg",
        "StopAreaNumber": 50242,
        "StopPointNumber": 50243,
        "StopPointDesignation": "D",
        "TimeTabledDateTime": "2015-02-17T14:01:56",
        "ExpectedDateTime": "2015-02-17T14:01:56"
      }
    ],
    "Metros": [
      {
        "SiteId": 9325,
        "JourneyDirection": 1,
        "Destination": "Hjulsta",
        "LineNumber": "10",
        "StopAreaName": "Sundbybergs centrum",
        "GroupOfLine": "Tunnelbanans blå linje",
        "DisplayTime": "Nu",
        "SafeDestinationName": "Hjulsta",
        "GroupOfLineId": 3,
        "DepartureGroupId": 1,
        "PlatformMessage": null,
        "TransportMode": "METRO"
      },
      {
        "SiteId": 9325,
        "JourneyDirection": 1,
        "Destination": "Hjulsta",
        "LineNumber": "10",
        "StopAreaName": "Sundbybergs centrum",
        "GroupOfLine": "Tunnelbanans blå linje",
        "DisplayTime": "11 min",
        "SafeDestinationName": "Hjulsta",
        "GroupOfLineId": 3,
        "DepartureGroupId": 1,
        "PlatformMessage": null,
        "TransportMode": "METRO"
      },
      {
        "SiteId": 9325,
        "JourneyDirection": 1,
        "Destination": "Hjulsta",
        "LineNumber": "10",
        "StopAreaName": "Sundbybergs centrum",
        "GroupOfLine": "Tunnelbanans blå linje",
        "DisplayTime": "21 min",
        "SafeDestinationName": "Hjulsta",
        "GroupOfLineId": 3,
        "DepartureGroupId": 1,
        "PlatformMessage": null,
        "TransportMode": "METRO"
      }
    ],
    "DataAge": 25,
    "LatestUpdate": "2015-02-17T13:05:47"
  },
  "ExecutionTime": 889,
  "Message": null,
  "StatusCode": 0
}
"""

SITE_JSON_TEST_INPUT = u"""
{
  "ResponseData": [
    {
      "Y": "59360842",
      "X": "17969256",
      "Type": "Station",
      "SiteId": "9325",
      "Name": "Sundbyberg (Sundbyberg)"
    }
  ],
  "ExecutionTime": 0,
  "Message": null,
  "StatusCode": 0
}
"""

SITE_JSON_TEST_INPUT_LONG = u"""
{
  "ResponseData": [
    {
      "Y": "59360842",
      "X": "17969256",
      "Type": "Station",
      "SiteId": "9325",
      "Name": "Sundbyberg (Sundbyberg)"
    },
    {
      "Y": "59360842",
      "X": "17969256",
      "Type": "Station",
      "SiteId": "9325",
      "Name": "Sundbybergs centrum (Sundbyberg)"
    },
    {
      "Y": "59360842",
      "X": "17969256",
      "Type": "Station",
      "SiteId": "9325",
      "Name": "Sundbybergs station (Sundbyberg)"
    }
  ],
  "ExecutionTime": 0,
  "Message": null,
  "StatusCode": 0
}
"""


class MyPrettyPrinter(pprint.PrettyPrinter):
    """
    Pretty printer subclass used for debugging parsing input.
    Avoids some unicode shanigans.
    """

    def format(self, object, context, maxlevels, level):
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


class ModelTest(unittest.TestCase):
    def test_compile_whitelist(self):
        expected = {'Buses': set(['518', '119']),
                    'Trains': set(['11', '10', '12'])}
        self.assertEqual(model.compile_whitelist({'trains': '10,11,12',
                                                  'buses': '119,518'}),
                         expected)

        expected = {'Buses': set(['518', '119']),
                    'Trains': set(['11', '10', '12']),
                    'Trams': set(['grisar'])}
        self.assertEqual(model.compile_whitelist({'trains': '10,11,12',
                                                  'buses': '119,518',
                                                  'crap': 'johnny',
                                                  'trams': 'grisar'}),
                         expected)

    def test_parse_displayrow(self):
        expected = [{u'destination': u'Hjulsta', u'displaytime': u'11 min', u'linenumber': u'10'},
                    {u'destination': u'Hjulsta', u'displaytime': u'21 min.', u'linenumber': u'10'}]
        self.assertEqual(model.parse_displayrow(u'10 Hjulsta 11 min, 10 Hjulsta 21 min.'),
                         expected)
        expected = [{u'linenumber': u'10',
                     u'destination': u'Kungsträdg.', u'displaytime': u'14 min.'}]
        self.assertEqual(model.parse_displayrow(u'10 Kungsträdg. 14 min.'),
                         expected)

        expected = [{u'linenumber': u'10',
                     u'destination': u'Kungsträdg.', u'displaytime': u'1 min'}]
        self.assertEqual(model.parse_displayrow(u'10 Kungsträdg. 1 min'),
                         expected)

        expected = [{u'linenumber': u'10',
                     u'destination': u'Kungsträdg.', u'displaytime': u'1 min'}]
        self.assertEqual(model.parse_displayrow(u'10  Kungsträdg. 1 min'),
                         expected)

        expected = []
        self.assertEqual(model.parse_displayrow(u'Korta tåg, vänligen gå mot mitten av plattformen. Short trains, please continue to the middle of the platform.'),
                         expected)

        expected = [{u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'01:49'},
                    {u'linenumber': u'10', u'destination': u'Kungsträdg.', u'displaytime': u'02:19'}]
        self.assertEqual(model.parse_displayrow(u'10 Kungsträdg. 01:49 10 Kungsträdg. 02:19'),
                         expected)

        expected = [{u'destination': u'Hjulsta', u'displaytime': u'8 min', u'linenumber': u'10'},
                    {u'destination': u'Hjulsta', u'displaytime': u'16 min.', u'linenumber': u'10'}]
        self.assertEqual(model.parse_displayrow(u'10 Hjulsta   8 min,      10 Hjulsta  16 min.'),
                         expected)

        self.assertEqual(model.parse_displayrow({}), [])

    @patch('slapi.model.get_now')
    def test_parse_response(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 1, 00, 30)
        expected = [{'transportmode': 'TRAIN', 'linenumber': '35', 'destination': 'Bålsta', 'displaytime': 'Nu', 'time': 0}, {'transportmode': 'METRO', 'linenumber': '10', 'destination': 'Hjulsta', 'displaytime': 'Nu', 'groupofline': 'Tunnelbanans blå linje', 'time': 0}, {'transportmode': 'TRAIN', 'linenumber': '35', 'destination': 'Västerhaninge', 'displaytime': '2 min', 'time': 2}, {'transportmode': 'BUS', 'linenumber': '504', 'destination': 'Rissne', 'displaytime': '4 min', 'groupofline': None, 'time': 4}, {'transportmode': 'BUS', 'linenumber': '152', 'destination': 'Liljeholmen', 'displaytime': '5 min', 'groupofline': None, 'time': 5}, {'transportmode': 'BUS', 'linenumber': '509', 'destination': 'Danderyds sjukhus', 'displaytime': '6 min', 'groupofline': None, 'time': 6}, {'transportmode': 'BUS', 'linenumber': '152', 'destination': 'Bromma flygplats', 'displaytime': '8 min', 'groupofline': None, 'time': 8}, {'transportmode': 'BUS', 'linenumber': '506', 'destination': 'Karolinska sjukhuset', 'displaytime': '9 min', 'groupofline': None, 'time': 9}, {'transportmode': 'BUS', 'linenumber': '506', 'destination': 'Hallonbergen', 'displaytime': '9 min', 'groupofline': None, 'time': 9}, {'transportmode': 'BUS', 'linenumber': '113', 'destination': 'Solna centrum', 'displaytime': '10 min', 'groupofline': None, 'time': 10}, {
            'transportmode': 'METRO', 'linenumber': '10', 'destination': 'Hjulsta', 'displaytime': '11 min', 'groupofline': 'Tunnelbanans blå linje', 'time': 11}, {'transportmode': 'BUS', 'linenumber': '509', 'destination': 'Brommaplan', 'displaytime': '12 min', 'groupofline': None, 'time': 12}, {'transportmode': 'TRAIN', 'linenumber': '35', 'destination': 'Kungsängen', 'displaytime': '14 min', 'time': 14}, {'transportmode': 'TRAIN', 'linenumber': '35', 'destination': 'Nynäshamn', 'displaytime': '17 min', 'time': 17}, {'transportmode': 'BUS', 'linenumber': '504', 'destination': 'Rissne', 'displaytime': '20 min', 'groupofline': None, 'time': 20}, {'transportmode': 'METRO', 'linenumber': '10', 'destination': 'Hjulsta', 'displaytime': '21 min', 'groupofline': 'Tunnelbanans blå linje', 'time': 21}, {'transportmode': 'BUS', 'linenumber': '506', 'destination': 'Karolinska sjukhuset', 'displaytime': '22 min', 'groupofline': None, 'time': 22}, {'transportmode': 'BUS', 'linenumber': '506', 'destination': 'Hallonbergen', 'displaytime': '24 min', 'groupofline': None, 'time': 24}, {'transportmode': 'TRAIN', 'linenumber': '35', 'destination': 'Bålsta', 'displaytime': '29 min', 'time': 29}, {'transportmode': 'BUS', 'linenumber': '509', 'destination': 'Brommaplan', 'displaytime': '29 min', 'groupofline': None, 'time': 29}]
        expected.sort(key=lambda x: x['time'])
        out = model.parse_json_response(DEPARTURE_JSON_TESTINPUT)
        out.sort(key=lambda x: x['time'])
        print(out)
        self.assertEqual(out, expected)

    @patch('slapi.model.get_now')
    def test_convert_time(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 1, 13, 2)
        self.assertEqual(model.convert_time('13:10'), 8)

        now_mock.return_value = datetime.datetime(2013, 12, 1, 23, 42)
        self.assertEqual(model.convert_time('00:15'), 33)

        now_mock.return_value = datetime.datetime(2013, 12, 1, 23, 42, 30)
        self.assertEqual(model.convert_time('23:42'), 0)

        self.assertEqual(model.convert_time('10 min'), 10)
        self.assertEqual(model.convert_time('1 min.'), 1)

        self.assertEqual(model.convert_time('100'), 100)

        self.assertEqual(model.convert_time('Nu'), 0)

        self.assertEqual(model.convert_time('-1 min'), -1)
        self.assertEqual(model.convert_time('-'), 0)

    @patch('slapi.model.requests')
    @patch('slapi.model.get_now')
    def test_get_departure(self, now_mock, req_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 1, 13, 2)
        req_mock.get = Mock()
        req_mock.get.return_value = Mock()
        req_mock.get.return_value.status_code = 500

        self.assertRaises(model.ApiException, model.get_departure,
                          'http://test/%s/%s', 31337, 'deadbeef')

        req_mock.get.return_value.status_code = 200
        req_mock.get.return_value.text = DEPARTURE_JSON_TESTINPUT

        out = model.get_departure('http://test/%s/%s', 31337, 'deadbeef')
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), 44)
        for item in out:
            self.assertEqual(type(item), dict)
            self.assertTrue(len(item) > 0)

    @patch('slapi.model.requests')
    @patch('slapi.model.get_now')
    def test_get_departures(self, now_mock, req_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 1, 13, 2)
        req_mock.get = Mock()
        req_mock.get.return_value = Mock()
        req_mock.get.return_value.status_code = 500

        self.assertRaises(model.ApiException, model.get_departures,
                          31337, 'deadbeef')

        responses = [DEPARTURE_JSON_TESTINPUT]

        def mock_get(*args):
            resp = Mock()
            resp.status_code = 200
            resp.text = responses.pop(0)
            return resp

        req_mock.get = mock_get

        out = model.get_departures(31337, 'deadbeef')
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), 44)
        for item in out:
            self.assertEqual(type(item), dict)
            self.assertTrue(len(item) > 0)

    @patch('slapi.model.get_now')
    def test_handle_flapping_displays(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 1, 00, 26)

        cached = [{u'destination': u'Kungsträdg.',
                   u'displaytime': u'5 min',
                   u'groupofline': u'Tunnelbanans blå linje',
                   u'linenumber': u'10',
                   u'stationname': u'Sundbybergs centrum',
                   u'time': 2,
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
                      u'time': 4,
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

        # let two minutes pass
        data = copy.deepcopy(cached)
        for d in data:
            d[u'time'] -= 2

        # first time, no flaps
        self.assertEqual(model.handle_flapping_displays('4711', data, {}),
                         [])

        # make the two hjulsta departures flap
        ts = datetime.datetime(2013, 12, 1, 00, 24)
        expected = []
        expected.append(data.pop(4))
        expected.append(data.pop(4))
        expected[0][u'firstseen'] = ts
        expected[1][u'firstseen'] = ts
        expected[0][u'firsttime'] = expected[0][u'time'] + 2
        expected[1][u'firsttime'] = expected[1][u'time'] + 2
        cache = {'4711': (ts, cached)}

        # expect them back
        self.assertEqual(model.handle_flapping_displays('4711', data, cache),
                         expected)

        # age the cache 10 mins, now only the 16 min departure is relevant
        ts = datetime.datetime(2013, 12, 1, 00, 24)
        cache = {'4711': (ts, cached)}
        expected.pop(0)
        expected[0][u'time'] -= 8
        expected[0][u'firstseen'] = ts
        expected[0][u'firsttime'] = expected[0][u'time'] + 10
        now_mock.return_value = datetime.datetime(2013, 12, 1, 00, 34)
        self.assertEqual(model.handle_flapping_displays('4711', data, cache),
                         expected)

    def test_parse_site_response(self):
        expected = [{u'name': u'Sundbyberg (Sundbyberg)'}]
        self.assertEqual(model.parse_json_site_response(SITE_JSON_TEST_INPUT),
                         expected)

        expected = [{u'name': u'Sundbyberg (Sundbyberg)'},
                    {u'name': u'Sundbybergs centrum (Sundbyberg)'},
                    {u'name': u'Sundbybergs station (Sundbyberg)'}]
        self.assertEqual(model.parse_json_site_response(SITE_JSON_TEST_INPUT_LONG),
                         expected)

        expected = []
        self.assertEqual(model.parse_json_site_response('{}'),
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

        model.cache.clear()

        responses = [SITE_JSON_TEST_INPUT]

        def mock_get(*args):
            resp = Mock()
            resp.status_code = 200
            resp.text = responses.pop(0)
            return resp

        req_mock.get = mock_get

        self.assertEqual(model.get_station_name(31337, 'deadbeef'),
                         u'Sundbyberg (Sundbyberg)')
