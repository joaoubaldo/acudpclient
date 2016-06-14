import struct


def readByte(f):
    return struct.unpack('B', f.read(1))[0]

def readSingle(f):
    return struct.unpack('<f', f.read(4))[0]

def readVector3f(f):
    return {'x':readSingle(f), 'y':readSingle(f), 'z':readSingle(f)}

def readString32(f):
    length = readByte(f)
    return f.read(length*4).decode('utf32')

def readString8(f):
    length = readByte(f)
    return f.read(length).decode('ascii')

def readUInt16(f):
    return struct.unpack('<H', f.read(2))[0]

def readUInt32(f):
    return struct.unpack('<L', f.read(4))[0]

def readInt32(f):
    return struct.unpack('<l', f.read(4))[0]
