# -*- coding: utf-8 -*-

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
        expected = [ {u'destination': u'Bålsta',
                      u'displaytime': u'Nu',
                      u'linenumber': u'35',
                      u'time': 0,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Hjulsta',
                      u'displaytime': u'Nu',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'time': 0,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'2 min',
                      u'linenumber': u'35',
                      u'time': 2,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Rissne',
                      u'displaytime': u'4 min',
                      u'groupofline': None,
                      u'linenumber': u'504',
                      u'time': 4,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Liljeholmen',
                      u'displaytime': u'5 min',
                      u'groupofline': None,
                      u'linenumber': u'152',
                      u'time': 5,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'6 min',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 6,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bromma flygplats',
                      u'displaytime': u'8 min',
                      u'groupofline': None,
                      u'linenumber': u'152',
                      u'time': 8,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'9 min',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 9,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'9 min',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 9,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'10 min',
                      u'groupofline': None,
                      u'linenumber': u'113',
                      u'time': 10,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hjulsta',
                      u'displaytime': u'11 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'time': 11,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'12 min',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 12,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Kungsängen',
                      u'displaytime': u'14 min',
                      u'linenumber': u'35',
                      u'time': 14,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Nynäshamn',
                      u'displaytime': u'17 min',
                      u'linenumber': u'35',
                      u'time': 17,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Rissne',
                      u'displaytime': u'20 min',
                      u'groupofline': None,
                      u'linenumber': u'504',
                      u'time': 20,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hjulsta',
                      u'displaytime': u'21 min',
                      u'groupofline': u'Tunnelbanans blå linje',
                      u'linenumber': u'10',
                      u'time': 21,
                      u'transportmode': u'METRO'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'22 min',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 22,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'24 min',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 24,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'29 min',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 29,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bålsta',
                      u'displaytime': u'29 min',
                      u'linenumber': u'35',
                      u'time': 29,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'13:15',
                      u'groupofline': None,
                      u'linenumber': u'515',
                      u'time': 765,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'13:24',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 774,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'13:27',
                      u'groupofline': None,
                      u'linenumber': u'113',
                      u'time': 777,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'13:30',
                      u'groupofline': None,
                      u'linenumber': u'515',
                      u'time': 780,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'13:39',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 789,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Västerhaninge',
                      u'displaytime': u'13:39',
                      u'linenumber': u'35',
                      u'time': 789,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Rissne',
                      u'displaytime': u'13:41',
                      u'groupofline': None,
                      u'linenumber': u'504',
                      u'time': 791,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Liljeholmen',
                      u'displaytime': u'13:42',
                      u'groupofline': None,
                      u'linenumber': u'152',
                      u'time': 792,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'13:44',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 794,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bromma flygplats',
                      u'displaytime': u'13:44',
                      u'groupofline': None,
                      u'linenumber': u'152',
                      u'time': 794,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'13:45',
                      u'groupofline': None,
                      u'linenumber': u'515',
                      u'time': 795,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Solna centrum',
                      u'displaytime': u'13:46',
                      u'groupofline': None,
                      u'linenumber': u'113',
                      u'time': 796,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'13:46',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 796,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'13:46',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 796,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Kungsängen',
                      u'displaytime': u'13:51',
                      u'linenumber': u'35',
                      u'time': 801,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Danderyds sjukhus',
                      u'displaytime': u'13:54',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 804,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Nynäshamn',
                      u'displaytime': u'13:54',
                      u'linenumber': u'35',
                      u'time': 804,
                      u'transportmode': u'TRAIN'},
                     {u'destination': u'Rissne',
                      u'displaytime': u'13:56',
                      u'groupofline': None,
                      u'linenumber': u'504',
                      u'time': 806,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Blackebergs gård',
                      u'displaytime': u'13:57',
                      u'groupofline': None,
                      u'linenumber': u'113',
                      u'time': 807,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Karolinska sjukhuset',
                      u'displaytime': u'13:59',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 809,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Odenplan',
                      u'displaytime': u'14:00',
                      u'groupofline': None,
                      u'linenumber': u'515',
                      u'time': 810,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Hallonbergen',
                      u'displaytime': u'14:01',
                      u'groupofline': None,
                      u'linenumber': u'506',
                      u'time': 811,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Brommaplan',
                      u'displaytime': u'14:01',
                      u'groupofline': None,
                      u'linenumber': u'509',
                      u'time': 811,
                      u'transportmode': u'BUS'},
                     {u'destination': u'Bålsta',
                      u'displaytime': u'14:06',
                      u'linenumber': u'35',
                      u'time': 816,
                      u'transportmode': u'TRAIN'}]
        expected.sort(key=lambda x: x['time'])
        out = model.parse_json_response(DEPARTURE_JSON_TESTINPUT)
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

        self.assertEquals(model.convert_time('Nu'), 0)

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
        req_mock.get.return_value.text = DEPARTURE_JSON_TESTINPUT

        out = model.get_departure('http://test/%s/%s', 31337, 'deadbeef')
        self.assertEquals(type(out), list)
        self.assertEquals(len(out), 44)
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

        responses = [DEPARTURE_JSON_TESTINPUT]

        def mock_get(*args):
            resp = Mock()
            resp.status_code = 200
            resp.text = responses.pop(0)
            return resp

        req_mock.get = mock_get

        out = model.get_departures(31337, 'deadbeef')
        self.assertEquals(type(out), list)
        self.assertEquals(len(out), 44)
        for item in out:
            self.assertEquals(type(item), dict)
            self.assertTrue(len(item) > 0)

    @patch('slapi.model.get_now')
    def test_handle_flapping_displays(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 00, 26)

        cached = [{ u'destination': u'Kungsträdg.',
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
        self.assertEquals(model.handle_flapping_displays('4711', data, {}),
                          [])

        # make the two hjulsta departures flap
        ts = datetime.datetime(2013, 12, 01, 00, 24)
        expected = []
        expected.append(data.pop(4))
        expected.append(data.pop(4))
        expected[0][u'firstseen'] = ts
        expected[1][u'firstseen'] = ts
        expected[0][u'firsttime'] = expected[0][u'time'] + 2
        expected[1][u'firsttime'] = expected[1][u'time'] + 2
        cache = {'4711': (ts, cached)}

        # expect them back
        self.assertEquals(model.handle_flapping_displays('4711', data, cache),
                          expected)

        # age the cache 10 mins, now only the 16 min departure is relevant
        ts = datetime.datetime(2013, 12, 01, 00, 24)
        cache = {'4711': (ts, cached)}
        expected.pop(0)
        expected[0][u'time'] -= 8
        expected[0][u'firstseen'] = ts
        expected[0][u'firsttime'] = expected[0][u'time'] + 10
        now_mock.return_value = datetime.datetime(2013, 12, 01, 00, 34)
        self.assertEquals(model.handle_flapping_displays('4711', data, cache),
                          expected)

    def test_parse_site_response(self):
        expected = [{u'name': u'Sundbyberg (Sundbyberg)'}]
        self.assertEquals(model.parse_json_site_response(SITE_JSON_TEST_INPUT),
                          expected)

        expected = [{u'name': u'Sundbyberg (Sundbyberg)'},
                    {u'name': u'Sundbybergs centrum (Sundbyberg)'},
                    {u'name': u'Sundbybergs station (Sundbyberg)'}]
        self.assertEquals(model.parse_json_site_response(SITE_JSON_TEST_INPUT_LONG),
                          expected)

        expected = []
        self.assertEquals(model.parse_json_site_response('{}'),
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

        self.assertEquals(model.get_station_name(31337, 'deadbeef'),
                          u'Sundbyberg (Sundbyberg)')
