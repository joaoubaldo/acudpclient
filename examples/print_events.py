from acudpclient.client import ACUDPClient

if __name__ == '__main__':
    client = ACUDPClient(port=10000, remote_port=10001)
    client.listen()
    client.get_session_info()
    while True:
        event = client.get_next_event(call_subscribers=False)
        print(event)