# ACUDPClient

ACUDPClient is module that can be used to communicate with an Assetto Corsa
server using its UDP protocol.


## Installation

```bash
$ python setup.py install
```

or

```bash
$ pip install acss
```

(virtualenv is recommended)


## Testing
```bash
$ nosetests
```

## Usage

Server events can be handled manually or using subscribers by calling
client's `get_next_event()` method.

When creating a subscriber implement methods for events that need to be
handled using the following naming scheme `on_<event_type>(self, event)`
where `event_type` is any of the types found in
`acudpclient.types.ACUDPProtoTypes` class (see Usage).


Manually handle events:
```python
from acudpclient.client import ACUDPClient

client = ACUDPClient(port=10000, remote_port=10001)
client.listen()

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
