import struct
import socket
import sys
from time import sleep
import logging
import io

from acudpclient.utils import *
from acudpclient.types import ACUDPProtoTypes


logging.basicConfig(level=logging.ERROR)
LOG = logging.getLogger("ac_udp_client")


class ACUDPClient(object):

    def __init__(self, port=10000, remote_port=10001, host='127.0.0.1'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('0.0.0.0', port)
        self.remote_port = remote_port
        self.host = host
        self._subscribers = {}

    def listen(self):
        self.sock.bind(self.server_address)
        self.sock.setblocking(0)
        self.file = io.open(self.sock.fileno(), mode='rb', buffering=4096)

    def subscribe(self, subscriber):
        if id(subscriber) in self._subscribers.keys():
            return False
        self._subscribers[id(subscriber)] = subscriber
        return True

    def unsubscribe(self, subscriber):
        if id(subscriber) not in self._subscribers.keys():
            return False
        del self._subscribers[id(subscriber)]
        return True

    def get_next_event(self, call_subscribers=True):
        event = ACUDPClient.consume_event(self.file)
        if event and call_subscribers:
            for subs in self._subscribers.itervalues():
                type_ = ACUDPProtoTypes.id_to_name(event['type'])
                method_name = 'on_%s' % (type_,)
                method = getattr(subs, method_name, None)
                if method and callable(method):
                    method(event)
        return event

    def broadcast_message(self, message):
        size = len(message)
        if size > 255:
            raise ValueError('Message is too large')
        data = struct.pack("BB%ds" % (size*4,),
                           ACUDPProtoTypes.ACSP_BROADCAST_CHAT,
                           size,
                           message.encode('utf32')
                          )
        self.sock.sendto(data, (self.host, self.remote_port))

    def send_message(self, car_id, message):
        size = len(message)
        if size > 255:
            raise ValueError('Message is too large')
        data = struct.pack("BBB%ds" % (size*4,),
                           ACUDPProtoTypes.ACSP_SEND_CHAT,
                           car_id,
                           size,
                           message.encode('utf32')
                          )
        self.sock.sendto(data, (self.host, self.remote_port))

    def get_car_info(self, car_id):
        data = struct.pack("BB",
            ACUDPProtoTypes.ACSP_GET_CAR_INFO,
            car_id
        )
        self.sock.sendto(data, (self.host, self.remote_port))

    def get_session_info(self, session_index=-1):
        data = struct.pack("<Bh",
            ACUDPProtoTypes.ACSP_GET_SESSION_INFO,
            session_index
        )
        self.sock.sendto(data, (self.host, self.remote_port))

    def enable_realtime_report(self, hz_ms=1000):
        data = struct.pack("<BH",
            ACUDPProtoTypes.ACSP_REALTIMEPOS_INTERVAL,
            hz_ms
        )
        self.sock.sendto(data, (self.host, self.remote_port))
