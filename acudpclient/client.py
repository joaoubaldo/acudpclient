"""
AC UDP Client module
"""
import struct
import socket
import logging
import io

from acudpclient.protocol import ACUDPConst
from acudpclient.packet_base import ACUDPPacket

logging.basicConfig(level=logging.ERROR)
LOG = logging.getLogger("ac_udp_client")


class ACUDPClient(object):
    """ This class represents the UDP Client """

    def __init__(self, port=10000, host='127.0.0.1', remote_port=10001):
        """ Constructor.

        Keyword arguments:
        port -- bind udp port
        host -- remote udp host (ac server)
        remote_port -- remote udp port (ac server)
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('0.0.0.0', port)
        self.remote_port = remote_port
        self.host = host
        self._subscribers = {}
        self.file = None

    def listen(self):
        """ Setup the listening socket """
        self.sock.bind(self.server_address)
        self.sock.setblocking(0)
        self.file = io.open(self.sock.fileno(), mode='rb', buffering=4096)

    def subscribe(self, subscriber):
        """ Register an event subscriber.

        Keyword arguments:
        subscriber -- subscriber instance

        Return True if the subscriber is successfuly registered,
        False if it's already registered. """
        if id(subscriber) in self._subscribers.keys():
            return False
        self._subscribers[id(subscriber)] = subscriber
        return True

    def unsubscribe(self, subscriber):
        """ Remove a subscriber.

        Keyword arguments:
        subscriber -- subscriber instance

        Return True if the subscriber is successfuly removed,
        False if the subscriber is found. """
        if id(subscriber) not in self._subscribers.keys():
            return False
        del self._subscribers[id(subscriber)]
        return True

    def get_next_event(self, call_subscribers=True):
        """ Consume an event from self.file and notify the subscribers.

        Keyword arguments:
        call_subscribers -- when True, subscribers get notified if there's
        an event

        Return the event object (subclass of ACUDPPacket) or None if there's
        no event ready. """
        event = ACUDPPacket.factory(self.file)
        if event and call_subscribers:
            for subs in self._subscribers.itervalues():
                method_name = 'on_%s' % (event.packet_name(),)
                method = getattr(subs, method_name, None)
                if method and callable(method):
                    method(event)
        return event

    def broadcast_message(self, message):
        """ Broadcast a message to server.

        Keyword arguments:
        message -- the message to send (limited to 255 characters) """
        size = len(message)
        if size > 255:
            raise ValueError('Message is too large')
        data = struct.pack("BB%ds" % (size*4,),
                           ACUDPConst.ACSP_BROADCAST_CHAT,
                           size,
                           message.encode('utf32'))
        sent = self.sock.sendto(data, (self.host, self.remote_port))
        if sent != len(data):
            raise ValueError('Not all bytes were sent.')

    def send_message(self, car_id, message):
        """ Send a message to a specific driver.

        Keyword arguments:
        car_id -- driver id that will receive the message
        message -- the message to send (limited to 255 characters) """
        size = len(message)
        if size > 255:
            raise ValueError('Message is too large')
        data = struct.pack("BBB%ds" % (size*4,),
                           ACUDPConst.ACSP_SEND_CHAT,
                           car_id,
                           size,
                           message.encode('utf32'))
        sent = self.sock.sendto(data, (self.host, self.remote_port))
        if sent != len(data):
            raise ValueError('Not all bytes were sent.')

    def get_car_info(self, car_id):
        """ Request CAR_INFO packet.

        Keyword arguments:
        car_id -- the driver id we want """
        data = struct.pack("BB",
                           ACUDPConst.ACSP_GET_CAR_INFO,
                           car_id)
        sent = self.sock.sendto(data, (self.host, self.remote_port))
        if sent != len(data):
            raise ValueError('Not all bytes were sent.')

    def get_session_info(self, session_index=-1):
        """ Request SESSION_INFO packet.

        Keyword arguments:
        session_index -- the session we want (default: -1 - current session)"""
        data = struct.pack("<Bh",
                           ACUDPConst.ACSP_GET_SESSION_INFO,
                           session_index)
        sent = self.sock.sendto(data, (self.host, self.remote_port))
        if sent != len(data):
            raise ValueError('Not all bytes were sent.')

    def enable_realtime_report(self, hz_ms=1000):
        """ Enable real time telemetry report.

        Keyword arguments:
        hz_ms -- the frequency we want to get reports, in milliseconds. Use 0
        to disable real time reporting (default: 1000) """
        data = struct.pack("<BH",
                           ACUDPConst.ACSP_REALTIMEPOS_INTERVAL,
                           hz_ms)
        sent = self.sock.sendto(data, (self.host, self.remote_port))
        if sent != len(data):
            raise ValueError('Not all bytes were sent.')
