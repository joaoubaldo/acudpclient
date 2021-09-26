from io import StringIO

import pytest 

from acudpclient.protocol import ACUDPConst
from acudpclient.packet_base import ACUDPPacket
import acudpclient.packets


def test_fail_with_invalid_type():
    file_obj = StringIO(u"invalid_type")
    with pytest.raises(NotImplementedError):
        ACUDPPacket.factory(file_obj)

def test_pass_with_valid_types():
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
        assert const in ACUDPPacket.packets()
        assert class_ == ACUDPPacket.packets().get(const)
