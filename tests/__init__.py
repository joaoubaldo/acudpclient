import sys
import base64
from StringIO import StringIO
import unittest

from acudpclient.client import ACUDPClient
from acudpclient.types import ACUDPProtoTypes
from acudpclient.packet_base import ACUDPPacket


class TestClient(unittest.TestCase):
    def test_consume_event(self):
        data = """OAQyBAAAAjFBAAAAQwAAACAAAAAhAAAAIAAAAEoAAABVAAAAIAAAADIAAAA0AAAALgAAADcAAAAg
            AAAAIQAAACAAAAAzAAAAMAAAAHEAAAB1AAAAYQAAAGwAAABpAAAAIAAAACEAAAAgAAAANwAAAHIA
            AABhAAAAYwAAAGUAAAAgAAAAIQAAACAAAABmAAAAYQAAAGMAAAB0AAAAbwAAAHIAAAB5AAAAIAAA
            AHQAAABjAAAAIAAAACYAAAAgAAAAYQAAAGIAAABzAAAABW1vbnphAAdRdWFsaWZ5Ah4AAAAAABkg
            BzNfY2xlYXIAAAAA"""
        data = StringIO(base64.b64decode(data))
        count = 0
        while 1:
            event = ACUDPPacket.consume_event(data)
            if event is None:
                break
            count += 1
        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()
