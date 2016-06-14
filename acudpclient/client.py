import struct
import socket
import sys
from time import sleep
import logging
import io

from acudpclient.utils import *
from acudpclient.types import ACUDPProtoTypes


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ac_udp_client")


class ACUDPClient(object):
    @classmethod
    def consume_event(cls, file_obj):
        try:
            type_ = readByte(file_obj)
        except struct.error:
            type_ = ""

        if type_ == "":
            return None

        act = ACUDPProtoTypes

        event = {'type': type_}

        try:
            if type_ == act.ACSP_VERSION:
                log.debug("ACSP_VERSION")
                event.update({'proto_version': readByte(file_obj)})
            elif type_ == act.ACSP_CAR_UPDATE:
                log.debug("ACSP_CAR_UPDATE")
                event.update({
                    'car_id': readByte(file_obj),
                    'pos': readVector3f(file_obj),
                    'vel': readVector3f(file_obj),
                    'gear': readByte(file_obj),
                    'engine_rpm': readUInt16(file_obj),
                    'normalized_spline_pos': readSingle(file_obj)
                })
            elif type_ == act.ACSP_CLIENT_EVENT:
                log.debug("ACSP_CLIENT_EVENT")
                ev_type = readByte(file_obj)  # ev_type
                car_id = readByte(file_obj)  # car id
                other_car_id = 255
                if ev_type == act.ACSP_CE_COLLISION_WITH_CAR:
                    other_car_id = readByte(file_obj)
                elif ev_type == act.ACSP_CE_COLLISION_WITH_ENV:
                    pass
                event.update({
                    'ev_type': ev_type,
                    'car_id': car_id,
                    'other_car_id': other_car_id,
                    'impact_speed': readSingle(file_obj),
                    'world_pos': readVector3f(file_obj),
                    'rel_pos': readVector3f(file_obj)
                })
            elif type_ == act.ACSP_CAR_INFO:
                log.debug("ACSP_CAR_INFO")
                event.update({
                    'car_id': readByte(file_obj),
                    'is_connected': readByte(file_obj) != 0,
                    'car_model': readString32(file_obj),
                    'car_skin': readString32(file_obj),
                    'driver_name': readString32(file_obj),
                    'driver_team': readString32(file_obj),
                    'driver_guid': readString32(file_obj),
                })
            elif type_ == act.ACSP_CHAT:
                log.debug("ACSP_CHAT")
                event.update({
                    'car_id': readByte(file_obj),
                    'message': readString32(file_obj)
                })
            elif type_ == act.ACSP_LAP_COMPLETED:
                log.debug("ACSP_LAP_COMPLETED")
                event.update({
                    'car_id': readByte(file_obj),
                    'lap_time': readUInt32(file_obj),
                    'cuts': readByte(file_obj),
                    'cars': []
                })
                cars_count = readByte(file_obj)
                for i in range(cars_count):
                    event['cars'].append({
                        'rcar_id': readByte(file_obj),
                        'rtime': readUInt32(file_obj),
                        'rlaps': readUInt16(file_obj)
                    })
                event['grip_level'] = readSingle(file_obj)
            elif type_ == act.ACSP_END_SESSION:
                log.debug("ACSP_END_SESSION")
                event.update({'filename': readString32(file_obj)})
            elif type_ == act.ACSP_CLIENT_LOADED:
                log.debug("ACSP_CLIENT_LOADED")
                event.update({'car_id': readByte(file_obj)})
            elif type_ == act.ACSP_CONNECTION_CLOSED:
                log.debug("ACSP_CONNECTION_CLOSED")
                event.update({
                    'driver_name': readString32(file_obj),
                    'driver_guid': readString32(file_obj),
                    'car_id': readByte(file_obj),
                    'car_model': readString8(file_obj),
                    'car_skin': readString8(file_obj)
                })
            elif type_ == act.ACSP_ERROR:
                log.debug("ACSP_ERROR")
                event.update({'message': readString32(file_obj)})
                log.error(event)
            elif type_ == act.ACSP_NEW_CONNECTION:
                log.debug("ACSP_NEW_CONNECTION")
                event.update({
                    'driver_name': readString32(file_obj),
                    'driver_guid': readString32(file_obj),
                    'car_id': readByte(file_obj),
                    'car_model': readString8(file_obj),
                    'car_skin': readString8(file_obj)
                })
            elif type_ == act.ACSP_NEW_SESSION \
            or type_ == act.ACSP_SESSION_INFO:
                log.debug("ACSP_SESSION_INFO")
                event.update({
                    'proto_version': readByte(file_obj),
                    'session_index': readByte(file_obj),
                    'current_sess_index': readByte(file_obj),
                    'session_count': readByte(file_obj),
                    'server_name': readString32(file_obj),
                    'track_name': readString8(file_obj),
                    'track_config': readString8(file_obj),
                    'name': readString8(file_obj),
                    'session_type': readByte(file_obj),
                    'time': readUInt16(file_obj),
                    'laps': readUInt16(file_obj),
                    'wait_time': readUInt16(file_obj),
                    'ambient_temp': readByte(file_obj),
                    'track_temp': readByte(file_obj),
                    'weather_graph': readString8(file_obj),
                    'elapsed_ms': readInt32(file_obj)
                })
            else:
                return None
        except UnicodeDecodeError:
            return None

        return event

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
