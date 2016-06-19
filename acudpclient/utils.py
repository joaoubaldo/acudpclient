"""
Utils module
"""
import logging

from acudpclient.types import UINT8
from acudpclient.packets import ACUDPPacket


LOG = logging.getLogger("ac_udp_utils")


def consume_event(file_obj):
    """
    Read an event from a file-like object.
    It first reads the packet type, as defined in AC UDP proto, then looks for
    it in the registered type classes. If type cannot be found, the exception
    NotImplementedError will be raised.
    Note: file_obj position will be changed after calling this function.

    Keyword arguments:
    file_obj -- file-like object to read the event from.

    Return event object (subclass of ACUDPPacket).
    """
    type_ = UINT8.get(file_obj)

    if type_ in ACUDPPacket.packets:
        cls_ = ACUDPPacket.packets[type_]
        return cls_.from_file(file_obj)
    else:
        raise NotImplementedError("Type not implemented %d" % (type_,))
