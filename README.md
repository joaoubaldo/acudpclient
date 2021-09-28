# ACUDPClient

[![Build Status](https://travis-ci.org/joaoubaldo/acudpclient.svg?branch=master)](https://travis-ci.org/joaoubaldo/acudpclient)

ACUDPClient is a Python module that can be used to communicate with an Assetto Corsa dedicated server.
Using its UDP protocol, real time telemetry, lap timings and session information is pushed to the client.
A few actions, like sending/broadcasting messages are also available.


## Installation

```bash
$ python setup.py install
```

or

```bash
$ pip install acudpclient
```

## Testing
```bash
$ pytest
```

## Usage

The client should be initialized like this:
```python
from acudpclient.client import ACUDPClient

client = ACUDPClient(port=10000, remote_port=10001, host='127.0.0.1')
client.listen()
```

* `remote_port` and `host` are used to send data to the AC server
* `listen()` will bind the server socket to `port`.

Server events can be handled directly or by event subscribers. In
both cases, `get_next_event()` method must be invoked in the
application's main loop.

When handling events directly, a call to `get_next_event()`
might return `None`, meaning there's no event available at that
point (the internal `ACUDPClient` socket is non-blocking).

When creating a subscriber class, specific events can be handled by creating
methods with the following naming scheme `on_<event_type>(self, event)`
where `event_type` is any of the types found in
`acudpclient.protocol.ACUDPConst` class (see Usage).

Events passed to `on_<event_type>(self, event)` are dictionaries containing
different keys depending on the event's type. Refer to `acudpclient.client import ACUDPClient`
to see which keys are available per event type.


## Examples

Handle events directly: `examples/print_events.py`

Handle events with a subscriber: `examples/print_events_pubsub.py`


### Capturing real data for testing purposes

1. Start the ACServer with UDP active.

2. Capture the data using `tcpdump`:
```bash
$ tcpdump -w /tmp/ac_out.pcap -s0 -i lo -n udp dst port 10000
```

3. Extract all udp payload from the pcap file:
```bash
$ tshark -r /tmp/ac_out.pcap -T fields -e data | tr -d '\n' | perl -pe 's/([0-9a-f]{2})/chr hex $1/gie' > /tmp/ac_out
```

4. `/tmp/ac_out` contains binary data sent by ACServer.
