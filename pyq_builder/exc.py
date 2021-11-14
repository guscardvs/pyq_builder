class PyQException(Exception):
    """Base PyQException"""


class UnsupportedClass(PyQException):
    """Received class is not supported for introspection"""
