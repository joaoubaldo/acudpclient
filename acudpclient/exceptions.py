""" This module contains custom exceptions used by acudpclient """


class ACUDPClientException(Exception):
    """ Base class for custom ACUDPClient exceptions. """
    pass


class NotEnoughBytes(ACUDPClientException):
    """ NotEnoughBytes exception. """
    pass
