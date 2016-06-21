""" This module declares core C types used by AC UDP protocol """

import struct


class ACUDPStruct(object):
    def __init__(self, fmt, formatter=lambda x: x):
        self.fmt = fmt
        self.formatter = formatter

    def size(self):
        return struct.calcsize(self.fmt)

    def get(self, file_obj):
        bytes_ = file_obj.read(self.size())
        data = struct.unpack(self.fmt, bytes_)
        if len(data) == 1:
            return self.formatter(data[0])
        return self.formatter(data)


class ACUDPString(object):
    def __init__(self, char_size, decoder=lambda x: x.decode('ascii')):
        self.char_size = char_size
        self.decoder = decoder

    def get(self, file_obj):
        size = UINT8.get(file_obj)
        bytes_ = file_obj.read(self.char_size*size)
        return self.decoder(bytes_)


class ACUDPConditionalStruct(object):
    def __init__(self, ac_struct, formatter=lambda x: x,
                 cond_func=lambda x: True, default=''):
        self.ac_struct = ac_struct
        self.cond_func = cond_func
        self.default = default
        self.formatter = formatter

    def size(self):
        return self.ac_struct.size()

    def get(self, file_obj, context=None):
        if not self.cond_func(context):
            return self.default
        return self.formatter(self.ac_struct.get(file_obj, context))


UINT8 = ACUDPStruct('B')
BOOL = ACUDPStruct('B', formatter=lambda x: x != 0)
UINT16 = ACUDPStruct('H')
INT16 = ACUDPStruct('h')
UINT32 = ACUDPStruct('I')
INT32 = ACUDPStruct('i')
FLOAT = ACUDPStruct('f')
VECTOR3F = ACUDPStruct('fff')
UTF32 = ACUDPString(4, decoder=lambda x: x.decode('utf32'))
ASCII = ACUDPString(1, decoder=lambda x: x.decode('ascii'))
