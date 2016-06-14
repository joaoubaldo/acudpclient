import base64
from StringIO import StringIO
import unittest

from acudpclient.client import ACUDPClient
from acudpclient.types import ACUDPProtoTypes


class TestClient(unittest.TestCase):
    def test_consume_event(self):
        data = """OAQyBAAAAjFBAAAAQwAAACAAAAAhAAAAIAAAAEoAAABVAAAAIAAAADIAAAA0AAAALgAAADcAAAAg
            AAAAIQAAACAAAAAzAAAAMAAAAHEAAAB1AAAAYQAAAGwAAABpAAAAIAAAACEAAAAgAAAANwAAAHIA
            AABhAAAAYwAAAGUAAAAgAAAAIQAAACAAAABmAAAAYQAAAGMAAAB0AAAAbwAAAHIAAAB5AAAAIAAA
            AHQAAABjAAAAIAAAACYAAAAgAAAAYQAAAGIAAABzAAAABW1vbnphAAdRdWFsaWZ5Ah4AAAAAABkg
            BzNfY2xlYXIAAAAA"""
        f = StringIO(base64.b64decode(data))
        event = ACUDPClient.consume_event(f)
        self.assertEqual(event['proto_version'], 4)
        self.assertEqual(event['type'], ACUDPProtoTypes.ACSP_VERSION)

        event = ACUDPClient.consume_event(f)
        self.assertEqual(event['track_temp'], 32)
        self.assertEqual(event['name'], u'Qualify')


if __name__ == '__main__':
    unittest.main()
