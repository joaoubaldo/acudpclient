"""
Collection of base classes to be used by packet related classes.
"""
import logging
import struct

from acudpclient.protocol import ACUDPConst
from acudpclient.types import *
from acudpclient.exceptions import NotEnoughBytes


LOG = logging.getLogger("ac_udp_packets")

class ACUDPPacket(object):
    """ This is the base class for AC UDP events, having a message type
    and byte data. Type and bytes should be defined at class level by each
    packet. """

    @classmethod
    def packets(cls):
        """ Return a dict of packet classes indexed by type """
        pkts = {}
        for subclass in cls.__subclasses__():
            pkts[getattr(subclass, '_type')] = subclass
        return pkts

    @classmethod
    def factory(cls, file_obj):
        """ Read an event from a file-like object.
        It first reads the packet type, as defined in AC UDP proto, then looks
        for it in the registered type classes. If type cannot be found, the
        exception NotImplementedError will be raised, otherwise from_file() is
        called on that type class.
        Note: file_obj position will be changed after calling this method.

        Keyword arguments:
        file_obj -- file-like object to read the event from.

        Return event object (subclass of ACUDPPacket).
        """
        try:
            type_ = UINT8.get(file_obj)
            if type_ in ACUDPPacket.packets():
                class_ = ACUDPPacket.packets()[type_]
                return class_.from_file(file_obj)
            else:
                raise NotImplementedError("Type not implemented %s" % (type_,))
        except struct.error:
            raise NotEnoughBytes

    @classmethod
    def from_file(cls, file_obj):
        """ Create a packet instance from bytes read from a file-like object.
        This class method is only meant to be called on subclasses that
        define _bytes and _type class properties.
        Note: file_obj position will be changed after calling this function.

        Keyword arguments:
        file_obj -- file-like object to read bytes from

        Return new packet instance.
        """
        instance = cls()
        for name, data_type in cls._bytes:
            val = data_type.get(file_obj, instance)
            setattr(instance, name, val)
        return instance

    def packet_name(self):
        """ Return the packet's type name. """
        return ACUDPConst.id_to_name(self._type)

    def __repr__(self):
        output = "<Packet(%s) %s>" % (
            ACUDPConst.id_to_name(self._type),
            ' '.join(["%s='%s'" % (name, repr(getattr(self, name, '')))
                      for name, _ in self._bytes])
            )
        return output.encode('utf-8')


class ACUDPPacketData(object):
    """ This class represents part of an AC UDP message (ACUDPPacket). It's
    specially useful to define a block of data that repeats. """

    @classmethod
    def from_file(cls, file_obj):
        """ Create a packet data instance from bytes read from a file-like
        object. This class method is only meant to be called on subclasses that
        define _bytes class properties (and not _type).

        Keyword arguments:
        file_obj -- file-like object to read bytes from

        Return new packet data instance.
        """
        instance = cls()
        for name, data_type in cls._bytes:
            val = data_type.get(file_obj)
            setattr(instance, name, val)
        return instance

    def __repr__(self):
        output = "<%s>" % (
            ' '.join(["%s='%s'" % (name, repr(getattr(self, name, '')))
                      for name, _ in self._bytes]))
        return output.encode('utf-8')


# Types
class Version(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_VERSION
    _bytes = (
        ('proto_version', UINT8),
    )


class CarUpdate(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_CAR_UPDATE
    _bytes = (
        ('car_id', UINT8),
        ('pos', VECTOR3F),
        ('vel', VECTOR3F),
        ('gear', UINT8),
        ('engine_rpm', UINT16),
        ('normalized_spline_pos', FLOAT)
    )


class ClientEvent(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_CLIENT_EVENT

    _bytes = (
        ('ev_type', UINT8),
        ('car_id', UINT8),
        ('other_car_id', ACUDPConditionalStruct(UINT8,
                                                cond_func=lambda packet: packet.ev_type == ACUDPConst.ACSP_CE_COLLISION_WITH_CAR,
                                                default=255)),
        ('impact_speed', FLOAT),
        ('world_pos', VECTOR3F),
        ('rel_pos', VECTOR3F)
    )


class CarInfo(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_CAR_INFO
    _bytes = (
        ('car_id', UINT8),
        ('is_connected', BOOL),
        ('car_model', UTF32),
        ('car_skin', UTF32),
        ('driver_name', UTF32),
        ('driver_team', UTF32),
        ('driver_guid', UTF32)
    )


class Chat(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_CHAT
    _bytes = (
        ('car_id', UINT8),
        ('message', UTF32)
    )


class LeaderboardEntry(ACUDPPacketData):
    """Packet data used in LapCompleted"""
    _bytes = (
        ('rcar_id', UINT8),
        ('rtime', UINT32),
        ('rlaps', UINT16),
        ('has_completed_flag', BOOL)
    )


class LapCompleted(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_LAP_COMPLETED
    _bytes = (
        ('car_id', UINT8),
        ('lap_time', UINT32),
        ('cuts', UINT8),
        ('cars', ACUDPPacketDataArray(LeaderboardEntry)),
        ('grip_level', FLOAT)
    )


class EndSession(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_END_SESSION
    _bytes = (
        ('filename', UTF32),
    )


class ClientLoaded(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_CLIENT_LOADED
    _bytes = (
        ('car_id', UINT8),
    )


class ConnectionClosed(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_CONNECTION_CLOSED
    _bytes = (
        ('driver_name', UTF32),
        ('driver_guid', UTF32),
        ('car_id', UINT8),
        ('car_model', ASCII),
        ('car_skin', ASCII)
    )


class Error(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_ERROR
    _bytes = (
        ('message', UTF32),
    )


class NewConnection(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_NEW_CONNECTION
    _bytes = (
        ('driver_name', UTF32),
        ('driver_guid', UTF32),
        ('car_id', UINT8),
        ('car_model', ASCII),
        ('car_skin', ASCII)
    )


class SessionInfo(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_SESSION_INFO
    _bytes = (
        ('proto_version', UINT8),
        ('session_index', UINT8),
        ('current_sess_index', UINT8),
        ('session_count', UINT8),
        ('server_name', UTF32),
        ('track_name', ASCII),
        ('track_config', ASCII),
        ('name', ASCII),
        ('session_type', UINT8),
        ('time', UINT16),
        ('laps', UINT16),
        ('wait_time', UINT16),
        ('ambient_temp', UINT8),
        ('track_temp', UINT8),
        ('weather_graph', ASCII),
        ('elapsed_ms', UINT32)
    )


class NewSession(ACUDPPacket):
    """Packet"""
    _type = ACUDPConst.ACSP_NEW_SESSION
    _bytes = (
        ('proto_version', UINT8),
        ('session_index', UINT8),
        ('current_sess_index', UINT8),
        ('session_count', UINT8),
        ('server_name', UTF32),
        ('track_name', ASCII),
        ('track_config', ASCII),
        ('name', ASCII),
        ('session_type', UINT8),
        ('time', UINT16),
        ('laps', UINT16),
        ('wait_time', UINT16),
        ('ambient_temp', UINT8),
        ('track_temp', UINT8),
        ('weather_graph', ASCII),
        ('elapsed_ms', UINT32)
    )
