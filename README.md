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

(virtualenv is recommended)


## Testing
```bash
$ nosetests
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

Handle events directly:
```python
from acudpclient.client import ACUDPClient

client = ACUDPClient(port=10000, remote_port=10001)
client.listen()

client.get_session_info()

while True:
  event = client.get_next_event(call_subscribers=False)
  print event
```


Handle events with a subscriber:
```python
from acudpclient.client import ACUDPClient

class ACEventHandler(object):
  def on_ACSP_LAP_COMPLETED(self, event):
    print event

  def on_ACSP_NEW_SESSION(self, event):
    print event

  def on_ACSP_NEW_CONNECTION(self, event):
    print event


handler = ACEventHandler()
client = ACUDPClient(port=10000, remote_port=10001)
client.listen()
client.subscribe(handler)

while True:
  client.get_next_event()
```
