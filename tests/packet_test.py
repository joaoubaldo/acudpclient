import os

from acudpclient.packet_base import ACUDPPacket
from acudpclient.exceptions import NotEnoughBytes


def test_pass_read_events():
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
    assert count == 395
