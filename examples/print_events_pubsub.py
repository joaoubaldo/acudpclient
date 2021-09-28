from acudpclient.client import ACUDPClient

class ACEventHandler(object):
  def on_ACSP_LAP_COMPLETED(self, event):
    print(event)

  def on_ACSP_NEW_SESSION(self, event):
    print(event)

  def on_ACSP_NEW_CONNECTION(self, event):
    print(event)

if __name__ == '__main__':
    handler = ACEventHandler()
    client = ACUDPClient(port=10000, remote_port=10001)
    client.listen()
    client.subscribe(handler)
    while True:
        client.get_next_event()