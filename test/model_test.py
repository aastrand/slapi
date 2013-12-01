# -*- coding: utf-8 -*-

import datetime
import unittest

from mock import patch

from slapi import model


METRO_TESTINPUT = u"""
<Departure xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www1.sl.se/realtidws/">
<LatestUpdate>2013-12-01T01:07:49.8525558+01:00</LatestUpdate>
<ExecutionTime>00:00:00.0156252</ExecutionTime>
<Buses/>
<Metros>
<Metro>
<SiteId>9325</SiteId>
<TransportMode>METRO</TransportMode>
<StationName>Sundbybergs centrum</StationName>
<GroupOfLine>Tunnelbanans blå linje</GroupOfLine>
<DisplayRow1>10 Kungsträdg. 11 min.</DisplayRow1>
<DisplayRow2>10 Kungsträdg. 01:49 10 Kungsträdg. 02:19</DisplayRow2>
</Metro>
<Metro>
<SiteId>9325</SiteId>
<TransportMode>METRO</TransportMode>
<StationName>Sundbybergs centrum</StationName>
<GroupOfLine>Tunnelbanans blå linje</GroupOfLine>
<DisplayRow1>10 Hjulsta 18 min.</DisplayRow1>
<DisplayRow2>10 Hjulsta 01:56 10 Hjulsta 02:26</DisplayRow2>
</Metro>
</Metros>
<Trains/>
<Trams/>
<TrainError>
<HasError>true</HasError>
<FaultCode>Client</FaultCode>
<ErrorLevel>Error</ErrorLevel>
<ErrorCode>1000</ErrorCode>
<ErrorSource>/realtidws/RealTimeService.asmx/GetDepartures</ErrorSource>
<ErrorMessage>Connection string is missing</ErrorMessage>
</TrainError>
<TramError>
<HasError>true</HasError>
<FaultCode>Client</FaultCode>
<ErrorLevel>Error</ErrorLevel>
<ErrorCode>1000</ErrorCode>
<ErrorSource>/realtidws/RealTimeService.asmx/GetDepartures</ErrorSource>
<ErrorMessage>Connection string is missing</ErrorMessage>
</TramError>
</Departure>
"""

TRAIN_TESTINPUT = u"""
<DPS xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www1.sl.se/realtidws/">
  <LatestUpdate>2013-12-01T12:32:41.1859002+01:00</LatestUpdate>
  <ExecutionTime>00:00:00.3593980</ExecutionTime>
  <Buses>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>515</LineNumber>
      <Destination>Odenplan</Destination>
      <TimeTabledDateTime>2013-12-01T12:40:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:40:00</ExpectedDateTime>
      <DisplayTime>12:40</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>504</LineNumber>
      <Destination>Stora Ursvik</Destination>
      <TimeTabledDateTime>2013-12-01T12:41:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:41:00</ExpectedDateTime>
      <DisplayTime>8 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Karolinska sjukhuset</Destination>
      <TimeTabledDateTime>2013-12-01T12:44:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:44:00</ExpectedDateTime>
      <DisplayTime>11 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Hallonbergen</Destination>
      <TimeTabledDateTime>2013-12-01T12:46:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:46:27</ExpectedDateTime>
      <DisplayTime>13 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>515</LineNumber>
      <Destination>Odenplan</Destination>
      <TimeTabledDateTime>2013-12-01T12:50:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:50:00</ExpectedDateTime>
      <DisplayTime>12:50</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Karolinska sjukhuset</Destination>
      <TimeTabledDateTime>2013-12-01T12:56:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:56:00</ExpectedDateTime>
      <DisplayTime>23 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>504</LineNumber>
      <Destination>Stora Ursvik</Destination>
      <TimeTabledDateTime>2013-12-01T12:56:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:56:00</ExpectedDateTime>
      <DisplayTime>23 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>515</LineNumber>
      <Destination>Odenplan</Destination>
      <TimeTabledDateTime>2013-12-01T13:00:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:00:00</ExpectedDateTime>
      <DisplayTime>13:00</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Hallonbergen</Destination>
      <TimeTabledDateTime>2013-12-01T13:01:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:01:00</ExpectedDateTime>
      <DisplayTime>28 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>515</LineNumber>
      <Destination>Odenplan</Destination>
      <TimeTabledDateTime>2013-12-01T13:10:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:10:00</ExpectedDateTime>
      <DisplayTime>13:10</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>504</LineNumber>
      <Destination>Stora Ursvik</Destination>
      <TimeTabledDateTime>2013-12-01T13:11:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:11:00</ExpectedDateTime>
      <DisplayTime>13:11</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Karolinska sjukhuset</Destination>
      <TimeTabledDateTime>2013-12-01T13:11:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:11:35</ExpectedDateTime>
      <DisplayTime>13:11</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Hallonbergen</Destination>
      <TimeTabledDateTime>2013-12-01T13:16:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:16:00</ExpectedDateTime>
      <DisplayTime>13:16</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>515</LineNumber>
      <Destination>Odenplan</Destination>
      <TimeTabledDateTime>2013-12-01T13:20:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:20:00</ExpectedDateTime>
      <DisplayTime>13:20</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Karolinska sjukhuset</Destination>
      <TimeTabledDateTime>2013-12-01T13:26:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:26:00</ExpectedDateTime>
      <DisplayTime>13:26</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>504</LineNumber>
      <Destination>Stora Ursvik</Destination>
      <TimeTabledDateTime>2013-12-01T13:26:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:26:00</ExpectedDateTime>
      <DisplayTime>13:26</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>515</LineNumber>
      <Destination>Odenplan</Destination>
      <TimeTabledDateTime>2013-12-01T13:30:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:30:00</ExpectedDateTime>
      <DisplayTime>13:30</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>12346</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs station</StopAreaName>
      <LineNumber>506</LineNumber>
      <Destination>Hallonbergen</Destination>
      <TimeTabledDateTime>2013-12-01T13:31:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:31:00</ExpectedDateTime>
      <DisplayTime>13:31</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Brommaplan</Destination>
      <TimeTabledDateTime>2013-12-01T12:29:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:32:31</ExpectedDateTime>
      <DisplayTime>0 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>152</LineNumber>
      <Destination>Bromma flygplats</Destination>
      <TimeTabledDateTime>2013-12-01T12:40:12</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:40:12</ExpectedDateTime>
      <DisplayTime>7 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Danderyds sjukhus</Destination>
      <TimeTabledDateTime>2013-12-01T12:40:36</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:41:47</ExpectedDateTime>
      <DisplayTime>9 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>152</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T12:43:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:43:18</ExpectedDateTime>
      <DisplayTime>10 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Brommaplan</Destination>
      <TimeTabledDateTime>2013-12-01T12:44:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:45:48</ExpectedDateTime>
      <DisplayTime>13 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>113</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T12:47:24</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:46:50</ExpectedDateTime>
      <DisplayTime>14 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Danderyds sjukhus</Destination>
      <TimeTabledDateTime>2013-12-01T12:55:36</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:55:36</ExpectedDateTime>
      <DisplayTime>12:55</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>113</LineNumber>
      <Destination>Blackebergs gård</Destination>
      <TimeTabledDateTime>2013-12-01T12:57:48</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:57:48</ExpectedDateTime>
      <DisplayTime>12:57</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Brommaplan</Destination>
      <TimeTabledDateTime>2013-12-01T12:59:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:00:09</ExpectedDateTime>
      <DisplayTime>27 min</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>152</LineNumber>
      <Destination>Bromma flygplats</Destination>
      <TimeTabledDateTime>2013-12-01T13:10:12</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:10:12</ExpectedDateTime>
      <DisplayTime>13:10</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Danderyds sjukhus</Destination>
      <TimeTabledDateTime>2013-12-01T13:10:36</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:10:36</ExpectedDateTime>
      <DisplayTime>13:10</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>152</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T13:13:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:13:06</ExpectedDateTime>
      <DisplayTime>13:13</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Brommaplan</Destination>
      <TimeTabledDateTime>2013-12-01T13:14:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:14:06</ExpectedDateTime>
      <DisplayTime>13:14</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>113</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T13:17:24</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:17:24</ExpectedDateTime>
      <DisplayTime>13:17</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Danderyds sjukhus</Destination>
      <TimeTabledDateTime>2013-12-01T13:25:36</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:25:36</ExpectedDateTime>
      <DisplayTime>13:25</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>113</LineNumber>
      <Destination>Blackebergs gård</Destination>
      <TimeTabledDateTime>2013-12-01T13:27:48</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:27:48</ExpectedDateTime>
      <DisplayTime>13:27</DisplayTime>
    </DpsBus>
    <DpsBus>
      <SiteId>9325</SiteId>
      <StopAreaNumber>50242</StopAreaNumber>
      <TransportMode>BUS</TransportMode>
      <StopAreaName>Sundbybergs torg</StopAreaName>
      <LineNumber>509</LineNumber>
      <Destination>Brommaplan</Destination>
      <TimeTabledDateTime>2013-12-01T13:29:06</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:29:06</ExpectedDateTime>
      <DisplayTime>13:29</DisplayTime>
    </DpsBus>
  </Buses>
  <Metros></Metros>
  <Trains>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Bålsta</Destination>
      <TimeTabledDateTime>2013-12-01T12:36:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:36:00</ExpectedDateTime>
      <DisplayTime>3 min</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Kungsängen</Destination>
      <TimeTabledDateTime>2013-12-01T12:51:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:51:00</ExpectedDateTime>
      <DisplayTime>18 min</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Bålsta</Destination>
      <TimeTabledDateTime>2013-12-01T13:06:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:06:00</ExpectedDateTime>
      <DisplayTime>13:06</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Kungsängen</Destination>
      <TimeTabledDateTime>2013-12-01T13:21:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:21:00</ExpectedDateTime>
      <DisplayTime>13:21</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>9002</LineNumber>
      <Destination>Fjärrtåg</Destination>
      <TimeTabledDateTime>2013-12-01T13:32:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:32:00</ExpectedDateTime>
      <DisplayTime>13:32</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Västerhaninge</Destination>
      <TimeTabledDateTime>2013-12-01T12:39:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:39:00</ExpectedDateTime>
      <DisplayTime>6 min</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Nynäshamn</Destination>
      <TimeTabledDateTime>2013-12-01T12:54:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:54:00</ExpectedDateTime>
      <DisplayTime>21 min</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Västerhaninge</Destination>
      <TimeTabledDateTime>2013-12-01T13:09:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:09:00</ExpectedDateTime>
      <DisplayTime>13:09</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
    </DpsTrain>
    <DpsTrain>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAIN</TransportMode>
      <StopAreaName>Sundbyberg</StopAreaName>
      <LineNumber>35</LineNumber>
      <Destination>Nynäshamn</Destination>
      <TimeTabledDateTime>2013-12-01T13:24:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:24:00</ExpectedDateTime>
      <DisplayTime>13:24</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
    </DpsTrain>
  </Trains>
  <Trams>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Alvik</Destination>
      <TimeTabledDateTime>2013-12-01T12:41:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:41:00</ExpectedDateTime>
      <DisplayTime>12:41</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Alvik</Destination>
      <TimeTabledDateTime>2013-12-01T12:56:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:56:00</ExpectedDateTime>
      <DisplayTime>12:56</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Alvik</Destination>
      <TimeTabledDateTime>2013-12-01T13:11:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:11:00</ExpectedDateTime>
      <DisplayTime>13:11</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Alvik</Destination>
      <TimeTabledDateTime>2013-12-01T13:26:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:26:00</ExpectedDateTime>
      <DisplayTime>13:26</DisplayTime>
      <JourneyDirection>2</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T12:39:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:43:00</ExpectedDateTime>
      <DisplayTime>10 min</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T12:54:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T12:54:00</ExpectedDateTime>
      <DisplayTime>12:54</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T13:09:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:09:00</ExpectedDateTime>
      <DisplayTime>13:09</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
    <DpsTram>
      <SiteId>9325</SiteId>
      <StopAreaNumber>0</StopAreaNumber>
      <TransportMode>TRAM</TransportMode>
      <StopAreaName>Sundbybergs centrum</StopAreaName>
      <LineNumber>22</LineNumber>
      <Destination>Solna centrum</Destination>
      <TimeTabledDateTime>2013-12-01T13:24:00</TimeTabledDateTime>
      <ExpectedDateTime>2013-12-01T13:24:00</ExpectedDateTime>
      <DisplayTime>13:24</DisplayTime>
      <JourneyDirection>1</JourneyDirection>
      <GroupOfLine>Tvärbanan</GroupOfLine>
    </DpsTram>
  </Trams>
</DPS>
"""


class ModelTest(unittest.TestCase):
    def test_parse_displayrow(self):
        expected = [{'destination': 'Hjulsta', 'displaytime': '11 min', 'linenumber': '10'},
                    {'destination': 'Hjulsta', 'displaytime': '21 min.', 'linenumber': '10'}]
        self.assertEquals(model.parse_displayrow('10 Hjulsta 11 min, 10 Hjulsta 21 min.'),
                          expected)
        expected = [{'linenumber': '10', 'destination': 'Kungstr\xc3\xa4dg.', 'displaytime': '14 min.'}]
        self.assertEquals(model.parse_displayrow('10 Kungsträdg. 14 min.'),
                          expected)

        expected = [{'linenumber': '10', 'destination': 'Kungstr\xc3\xa4dg.', 'displaytime': '1 min'}]
        self.assertEquals(model.parse_displayrow('10 Kungsträdg. 1 min'),
                          expected)

        expected = [{'linenumber': '10', 'destination': 'Kungstr\xc3\xa4dg.', 'displaytime': '1 min'}]
        self.assertEquals(model.parse_displayrow('10  Kungsträdg. 1 min'),
                          expected)

        expected = []
        self.assertEquals(model.parse_displayrow('Korta tåg, vänligen gå mot mitten av plattformen. Short trains, please continue to the middle of the platform.'),
                          expected)

        expected = [{'linenumber': '10', 'destination': 'Kungstr\xc3\xa4dg.', 'displaytime': '01:49'},
                    {'linenumber': '10', 'destination': 'Kungstr\xc3\xa4dg.', 'displaytime': '02:19'}]
        self.assertEquals(model.parse_displayrow('10 Kungsträdg. 01:49 10 Kungsträdg. 02:19'),
                          expected)

    @patch('slapi.model.get_now')
    def test_parse_response(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 00, 30)
        expected = [{'destination': 'Kungstr\xc3\xa4dg.',
                     'displaytime': '11 min.',
                     'groupofline': 'Tunnelbanans bl\xc3\xa5 linje',
                     'linenumber': '10',
                     'stationname': 'Sundbybergs centrum',
                     'time': 11,
                     'transportmode': 'METRO'},
                    {'destination': 'Hjulsta',
                     'displaytime': '18 min.',
                     'groupofline': 'Tunnelbanans bl\xc3\xa5 linje',
                     'linenumber': '10',
                     'stationname': 'Sundbybergs centrum',
                     'time': 18,
                     'transportmode': 'METRO'},
                    {'destination': 'Kungstr\xc3\xa4dg.',
                     'displaytime': '01:49',
                     'groupofline': 'Tunnelbanans bl\xc3\xa5 linje',
                     'linenumber': '10',
                     'stationname': 'Sundbybergs centrum',
                     'time': 79,
                     'transportmode': 'METRO'},
                    {'destination': 'Hjulsta',
                     'displaytime': '01:56',
                     'groupofline': 'Tunnelbanans bl\xc3\xa5 linje',
                     'linenumber': '10',
                     'stationname': 'Sundbybergs centrum',
                     'time': 86,
                     'transportmode': 'METRO'},
                    {'destination': 'Kungstr\xc3\xa4dg.',
                     'displaytime': '02:19',
                     'groupofline': 'Tunnelbanans bl\xc3\xa5 linje',
                     'linenumber': '10',
                     'stationname': 'Sundbybergs centrum',
                     'time': 109,
                     'transportmode': 'METRO'},
                    {'destination': 'Hjulsta',
                     'displaytime': '02:26',
                     'groupofline': 'Tunnelbanans bl\xc3\xa5 linje',
                     'linenumber': '10',
                     'stationname': 'Sundbybergs centrum',
                     'time': 116,
                     'transportmode': 'METRO'}]
        self.assertEquals(model.parse_xml_response(METRO_TESTINPUT), expected)

    @patch('slapi.model.get_now')
    def test_parse_train_response(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 11, 30)
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(model.parse_xml_response(TRAIN_TESTINPUT))

    @patch('slapi.model.get_now')
    def test_convert_time(self, now_mock):
        now_mock.return_value = datetime.datetime(2013, 12, 01, 13, 02)
        self.assertEquals(model.convert_time('13:10'), 8)

        now_mock.return_value = datetime.datetime(2013, 12, 01, 23, 42)
        self.assertEquals(model.convert_time('00:15'), 33)
