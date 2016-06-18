"""
Module where AC UDP packets are defined.
"""
import logging

from acudpclient.types import Uint8
from acudpclient.types import Uint16
from acudpclient.types import Uint32
from acudpclient.types import Float
from acudpclient.types import Vector3f
from acudpclient.types import UTF32
from acudpclient.types import ASCII
from acudpclient.types import ACUDPProtoTypes
from acudpclient.types import ACUDPConditionalStruct
from acudpclient.packet_base import ACUDPPacket
from acudpclient.packet_base import ACUDPPacketData
from acudpclient.packet_base import ACUDPPacketDataArray

LOG = logging.getLogger("ac_udp_packets")


class Version(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_VERSION
    _bytes = (
        ('proto_version', Uint8),
    )

class CarUpdate(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_CAR_UPDATE
    _bytes = (
        ('car_id', Uint8),
        ('pos', Vector3f),
        ('vel', Vector3f),
        ('gear', Uint8),
        ('engine_rpm', Uint16),
        ('normalized_spline_pos', Float)
    )


class ClientEvent(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_CLIENT_EVENT
    _bytes = (
        ('ev_type', Uint8),
        ('car_id', Uint8),
        ('other_car_id', ACUDPConditionalStruct(Uint8,
                                                cond_func=lambda x: True \
                if x.ev_type == ACUDPProtoTypes.ACSP_CE_COLLISION_WITH_CAR \
                else False,
                                                default=255)),
        ('impact_speed', Float),
        ('world_pos', Vector3f),
        ('rel_pos', Vector3f)
    )


class CarInfo(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_CAR_INFO
    _bytes = (
        ('car_id', Uint8),
        ('is_connected', Uint8),
        ('car_model', UTF32),
        ('car_skin', UTF32),
        ('driver_name', UTF32),
        ('driver_team', UTF32),
        ('driver_guid', UTF32)
    )

class Chat(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_CHAT
    _bytes = (
        ('car_id', Uint8),
        ('message', UTF32)
    )


class LeaderboardEntry(ACUDPPacketData):
    """Packet data used in LapCompleted"""
    _bytes = (
        ('rcar_id', Uint8),
        ('rtime', Uint32),
        ('rlaps', Uint16)
    )


class LapCompleted(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_LAP_COMPLETED
    _bytes = (
        ('car_id', Uint8),
        ('lap_time', Uint32),
        ('cuts', Uint8),
        ('cars', ACUDPPacketDataArray(LeaderboardEntry)),
        ('grip_level', Float)
    )

class EndSession(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_END_SESSION
    _bytes = (
        ('filename', UTF32),
    )


class ClientLoaded(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_CLIENT_LOADED
    _bytes = (
        ('car_id', Uint8),
    )


class ConnectiontClosed(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_CONNECTION_CLOSED
    _bytes = (
        ('driver_name', UTF32),
        ('driver_guid', UTF32),
        ('car_id', Uint8),
        ('car_model', ASCII),
        ('car_skin', ASCII)
    )


class Error(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_ERROR
    _bytes = (
        ('message', UTF32),
    )


class NewConnection(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_NEW_CONNECTION
    _bytes = (
        ('driver_name', UTF32),
        ('driver_guid', UTF32),
        ('car_id', Uint8),
        ('car_model', ASCII),
        ('car_skin', ASCII)
    )


class SessionInfo(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_SESSION_INFO
    _bytes = (
        ('proto_version', Uint8),
        ('session_index', Uint8),
        ('current_sess_index', Uint8),
        ('session_count', Uint8),
        ('server_name', UTF32),
        ('track_name', ASCII),
        ('track_config', ASCII),
        ('name', ASCII),
        ('session_type', Uint8),
        ('time', Uint16),
        ('laps', Uint16),
        ('wait_time', Uint16),
        ('ambient_temp', Uint8),
        ('track_temp', Uint8),
        ('weather_graph', ASCII),
        ('elapsed_ms', Uint32)
    )


class NewSession(ACUDPPacket):
    """Packet"""
    _type = ACUDPProtoTypes.ACSP_NEW_SESSION
    _bytes = (
        ('proto_version', Uint8),
        ('session_index', Uint8),
        ('current_sess_index', Uint8),
        ('session_count', Uint8),
        ('server_name', UTF32),
        ('track_name', ASCII),
        ('track_config', ASCII),
        ('name', ASCII),
        ('session_type', Uint8),
        ('time', Uint16),
        ('laps', Uint16),
        ('wait_time', Uint16),
        ('ambient_temp', Uint8),
        ('track_temp', Uint8),
        ('weather_graph', ASCII),
        ('elapsed_ms', Uint32)
    )
