import sys
import base64
from StringIO import StringIO
import unittest

from acudpclient.client import ACUDPClient
from acudpclient.protocol import ACUDPConst
from acudpclient.packet_base import ACUDPPacket
from acudpclient.exceptions import NotEnoughBytes
import acudpclient.packets


def test_server():
    import socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 10002))


class TestClient(unittest.TestCase):
    def test_event_factory(self):
        data = """OAQyBAAAAjFBAAAAQwAAACAAAAAhAAAAIAAAAEoAAABVAAAAIAAAADIAAAA0AAAALgAAADcAAAAg
            AAAAIQAAACAAAAAzAAAAMAAAAHEAAAB1AAAAYQAAAGwAAABpAAAAIAAAACEAAAAgAAAANwAAAHIA
            AABhAAAAYwAAAGUAAAAgAAAAIQAAACAAAABmAAAAYQAAAGMAAAB0AAAAbwAAAHIAAAB5AAAAIAAA
            AHQAAABjAAAAIAAAACYAAAAgAAAAYQAAAGIAAABzAAAABW1vbnphAAdRdWFsaWZ5Ah4AAAAAABkg
            BzNfY2xlYXIAAAAA"""
        file_obj = StringIO(base64.b64decode(data))
        count = 0
        while 1:
            try:
                event = ACUDPPacket.factory(file_obj)
            except NotEnoughBytes:
                break
            else:
                count += 1
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
