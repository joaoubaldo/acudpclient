import os
import sys
import base64
from StringIO import StringIO
import unittest

from acudpclient.client import ACUDPClient
from acudpclient.protocol import ACUDPConst
from acudpclient.packet_base import ACUDPPacket
from acudpclient.exceptions import NotEnoughBytes
import acudpclient.packets


class TestClient(unittest.TestCase):
    def test_event_factory(self):
        raw_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'ac_out')
        file_obj = open(raw_file, 'rb')
        count = 0
        while 1:
            try:
                event = ACUDPPacket.factory(file_obj)
            except NotEnoughBytes:
                break
            else:
                count += 1
        self.assertEqual(count, 395)

    def test_invalid_type(self):
        file_obj = StringIO("invalid_type")
        self.assertRaises(NotImplementedError, ACUDPPacket.factory, file_obj)

    def test_type_id(self):
        p = """ACSP_CAR_INFO        CarInfo
            ACSP_CAR_UPDATE         CarUpdate
            ACSP_CHAT               Chat
            ACSP_CLIENT_EVENT       ClientEvent
            ACSP_CLIENT_LOADED      ClientLoaded
            ACSP_CONNECTION_CLOSED  ConnectionClosed
            ACSP_END_SESSION        EndSession
            ACSP_ERROR              Error
            ACSP_LAP_COMPLETED      LapCompleted
            ACSP_NEW_CONNECTION     NewConnection
            ACSP_NEW_SESSION        NewSession
            ACSP_SESSION_INFO       SessionInfo
            ACSP_VERSION            Version"""

        for type_class in p.splitlines():
            fields = type_class.strip().split(" ")
            fields[0], fields[-1]
            const = getattr(ACUDPConst, fields[0])
            class_ = getattr(acudpclient.packets, fields[-1])
            self.assertIn(const, ACUDPPacket.packets())
            self.assertEqual(class_, ACUDPPacket.packets().get(const))


if __name__ == '__main__':
    unittest.main()
