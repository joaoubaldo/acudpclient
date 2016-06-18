"""
Utils module
"""
import logging

from acudpclient.types import UINT8
from acudpclient.packets import ACUDPPacket


LOG = logging.getLogger("ac_udp_utils")


def consume_event(file_obj):
    """
    Read event from file-like object buffer. File position will be changed.
    """
    try:
        type_ = UINT8.get(file_obj)
    except Exception:
        return None

    if type_ in ACUDPPacket.packets:
        cls_ = ACUDPPacket.packets[type_]
        try:
            return cls_.from_file(file_obj)
        except Exception, exc:
            LOG.error(exc)
            return None
    else:
        raise NotImplementedError("Type not implemented %d" % (type_,))
