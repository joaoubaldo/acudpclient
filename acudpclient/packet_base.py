import logging

from acudpclient.types import Uint8


LOG = logging.getLogger("ac_udp_packets")


class ACUDPPacket(object):
    @classmethod
    def from_file(cls, file_obj):
        instance = cls()
        for name, data_type in cls._bytes:
            val = data_type.get(file_obj, context=instance)
            setattr(instance, name, val)
        return instance

    class __metaclass__(type):
        packets = {}

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            if len(klass.mro()[1:-1]) == 1:
                meta.packets[klass._type] = klass
                LOG.info("Registered new packet %s" % (name,))
            return klass

    def __repr__(self):
        s = "<Packet(%s) %s>" % (ACUDPProtoTypes.id_to_name(self._type),
            ' '.join(["%s='%s'" % (name, repr(getattr(self, name, ''))) \
                    for name, bytes_ in self._bytes]))
        return s.encode('utf-8')


class ACUDPPacketData(object):
    @classmethod
    def from_file(cls, file_obj):
        instance = cls()
        for name, data_type in cls._bytes:
            val = data_type.get(file_obj, context=instance)
            setattr(instance, name, val)
        return instance


    def __repr__(self):
        s = "<%s>" % (
            ' '.join(["%s='%s'" % (name, repr(getattr(self, name, ''))) \
                for name, bytes_ in self._bytes]))
        return s.encode('utf-8')


class ACUDPPacketDataArray(object):
    def __init__(self, packet_data):
        self.packet_data = packet_data

    def get(self, f, context=None):
        size = Uint8.get(f)
        res = []
        for i in range(size):
            res.append(self.packet_data.from_file(f))
        return res
