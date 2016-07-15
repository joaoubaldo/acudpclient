""" This module declares core C types used by AC UDP protocol """
import struct


class ACUDPStruct(object):
    """ This class wraps struct module functionality and provides ways to
    read formatted bytes from a file-like object """
    def __init__(self, fmt, formatter=lambda x: x):
        """ Constructor.

        Keyword arguments:
        fmt -- struct-like string representing bytes
        formatter -- function called after each file_obj read. It accepts one
        argument - the read bytes
        """
        self.fmt = fmt
        self.formatter = formatter

    def size(self):
        """ Return computed size in bytes of self.fmt string """
        return struct.calcsize(self.fmt)

    def get(self, file_obj):
        """ Read self.size() bytes from a file-like object and unpack them
        with self.fmt.

        Keyword arguments:
        file_obj -- file-like object

        Return output of self.formatter (default: string with read bytes).
        """
        bytes_ = file_obj.read(self.size())
        data = struct.unpack(self.fmt, bytes_)
        if len(data) == 1:
            return self.formatter(data[0])
        return self.formatter(data)


class ACUDPString(object):
    """ This class represents a AC UDP String. """
    def __init__(self, char_size=1, decoder=lambda x: x.decode('ascii')):
        """ Constructor.

        Keyword arguments:
        char_size -- size in bytes of a char (ascii = 1)
        decoder -- function used to decode the bytes. It accepts one
        argument x, the read bytes (default: x.decode('ascii'))
        """
        self.char_size = char_size
        self.decoder = decoder

    def get(self, file_obj):
        """ Read a string from a file-like object.
        First reads a byte that tells the string length (255 max char limit).
        It then reads the actual string.

        Keyword arguments:
        file_obj -- file-like object

        Return output of self.decoder (default: ascii encoded string).
        """
        size = UINT8.get(file_obj)
        bytes_ = file_obj.read(self.char_size*size)
        return self.decoder(bytes_)


class ACUDPConditionalStruct(object):
    """ Wrapper around ACUDPStruct. """
    def __init__(self, ac_struct, cond_func=lambda x: True, default=''):
        """ Constructor.

        Keyword arguments:
        ac_struct -- ACUDPStruct-like object
        cond_func -- condition check function. Accepts context as an argument.
        (defaut: True).
        default -- value to return in case cond_func returns False
        """
        self.ac_struct = ac_struct
        self.cond_func = cond_func
        self.default = default

    def size(self):
        """ Return ac_struct fmt size. """
        return self.ac_struct.size()

    def get(self, file_obj, context=None):
        """
        Keyword arguments:
        file_obj -- file-like object
        context -- user defined data.

        Return ACUDPStruct.get() output if self.cond_func returns True,
        otherwise return self.default.
        """

        if not self.cond_func(context):
            return self.default
        return self.ac_struct.get(file_obj, context)


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
