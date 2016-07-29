import sys

from acudpclient import packets
from acudpclient.packet_base import ACUDPPacket
from acudpclient.exceptions import NotEnoughBytes

if len(sys.argv) != 2:
    sys.exit(1)

f = open(sys.argv[1], 'rb')

while 1:
    try:
        event = ACUDPPacket.factory(f)
        print event
    except NotEnoughBytes:
        break
