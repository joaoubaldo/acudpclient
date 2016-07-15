""" AC protocol properties """


class ACUDPConst(object):
    """ Constants used in AC UDP protocol """
    ACSP_ADMIN_COMMAND = 209
    ACSP_BROADCAST_CHAT = 203
    ACSP_CAR_INFO = 54
    ACSP_CAR_UPDATE = 53
    ACSP_CE_COLLISION_WITH_CAR = 10
    ACSP_CE_COLLISION_WITH_ENV = 11
    ACSP_CHAT = 57
    ACSP_CLIENT_EVENT = 130
    ACSP_CLIENT_LOADED = 58
    ACSP_CONNECTION_CLOSED = 52
    ACSP_END_SESSION = 55
    ACSP_ERROR = 60
    ACSP_GET_CAR_INFO = 201
    ACSP_GET_SESSION_INFO = 204
    ACSP_KICK_USER = 206
    ACSP_LAP_COMPLETED = 73
    ACSP_NEW_CONNECTION = 51
    ACSP_NEW_SESSION = 50
    ACSP_NEXT_SESSION = 207
    ACSP_REALTIMEPOS_INTERVAL = 200
    ACSP_RESTART_SESSION = 208
    ACSP_SEND_CHAT = 202
    ACSP_SESSION_INFO = 59
    ACSP_SET_SESSION_INFO = 205
    ACSP_VERSION = 56

    @classmethod
    def id_to_name(cls, id_):
        """ Convert a constant id to name.

        Keyword arguments:
        id_ -- constant id

        Return constant name.
        """
        for attr in cls.__dict__:
            if attr.startswith('ACSP_'):
                if getattr(cls, attr) == id_:
                    return attr
        return None
