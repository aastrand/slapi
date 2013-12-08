slapi
=====

Aggregating API and view for the trafiklab realtime APIs

## About

This API is inspired by [SB\_SL](https://github.com/carlfranzon/SB_SL). I wanted caching, some filtering and prefer python to PHP, so I wrote this. Images and idea totally stolen from him though.

It tries to be a HTTP REST JSON/HTML API aggregator for the [trafiklab APIs](http://http://www.trafiklab.se/api/sl-realtidsinfo).

The HTML renderer can be used as a backend for [Status Board](https://itunes.apple.com/us/app/status-board/id449955536?mt=8&ign-mpt=uo%3D4) custom tables.

![Screenshot](https://dl.dropboxusercontent.com/u/7823835/dashboard2.PNG)

## Installation

1) Install the requirements using pip: 

```
$ pip install -r requirements.txt
```

2) To run the flask server as is:

```
$ PYTHONPATH=. python slapi/app.py
```

I recommend running it some WSGI container. I personally [run flask inside apache](http://flask.pocoo.org/docs/deploying/mod_wsgi/) using mod_wsgi.


3) Add queries to whatever you have reading the API. In Status Board, add a URL like below to a custom Table widget:

```
http://yourhost.se:port/station-id?key=key&distance=5&buses=none&trams=none
```

The station ID is a [unique integer ID](http://console.apihq.com/sl-realtidsinformation) for the station you want departures for.
 

## API arguments

The API path is simply the station id (see above), the arguments are as follows:

| Name      | Typ                 | Optional? | Description |
| -------- |:-------------------- |:--------- | ----------- |
| key      | string               | no        | Trafiklab API key. See trafiklabs site on how to get one. |
| distance | integer              | yes       | How long it takes to get to the station in minutes. Will filter departures that leave in less time. |
| limit    | integer              | yes       | Return at most this many results, regardless of how many available departures there are. |
| alt      | string               | yes       | Return in alternative format. Valid values: json |
| buses    | comma separated list | yes       | Only show these lines for this transportation type. Example: buses=10,20,30. |
| metros   | comma separated list | yes       | Only show these lines for this transportation type. Example: metros=10,20,30. |
| trains   | comma separated list | yes       | Only show these lines for this transportation type. Example: trains=10,20,30. |
| trams    | comma separated list | yes       | Only show these lines for this transportation type. Example: trams=10,20,30. |


## Bugs

Much like SB_SL, I havn't tested it on every possible station and you might encounter weirdness. Contributions welcome if so.