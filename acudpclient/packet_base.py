"""
Collection of base classes to be used by packet related classes.
"""
import logging
import struct

from acudpclient.protocol import ACUDPConst
from acudpclient.types import UINT8
from acudpclient.exceptions import NotEnoughBytes


LOG = logging.getLogger("ac_udp_packets")


class ACUDPPacketMeta(type):
    """ This is the Metaclass for ACUDPPacket, that tracks all of its
    subclasses. """
    packets = {}

    def __new__(mcs, name, bases, dct):
        klass = type.__new__(mcs, name, bases, dct)

        if len(klass.mro()[1:-1]) == 1:
            LOG.info("Registered new packet %s", name)
            mcs.packets[dct.get('_type')] = klass
        return klass


class ACUDPPacket(object):
    """ This is the base class for AC UDP events, having a message type
    and byte data. Type and bytes should be defined at class level by each
    packet. """
    __metaclass__ = ACUDPPacketMeta

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
            if type_ in ACUDPPacket.packets:
                class_ = ACUDPPacket.packets[type_]
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
            val = data_type.get(file_obj)
            setattr(instance, name, val)
        return instance

    def __repr__(self):
        output = "<Packet(%s) %s>" % (
            ACUDPConst.id_to_name(self._type),
            ' '.join(["%s='%s'" % (name, repr(getattr(self, name, ''))) \
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
            ' '.join(["%s='%s'" % (name, repr(getattr(self, name, ''))) \
                for name, _ in self._bytes]))
        return output.encode('utf-8')


class ACUDPPacketDataArray(object):
    """ This class represents an array of packet data (ACUDPPacketData). """
    def __init__(self, packet_data):
        self.packet_data = packet_data

    def get(self, file_obj):
        """ Reads next byte as a byte representing the total number of packet
        data blocks that exist in the buffer and reads them.

        Keyword arguments:
        file_obj -- file-like object to read bytes from

        Return list of read ACUDPPacketData blocks.
        """
        size = UINT8.get(file_obj)
        res = []
        for _ in range(size):
            res.append(self.packet_data.from_file(file_obj))
        return res
