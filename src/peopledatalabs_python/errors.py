"""
Exceptions raised by the client.
"""


class EmptyParametersException(Exception):
    """
    Thrown when an API method is invoked with no parameters.
    """


class InvalidEndpointError(Exception):
    """
    Thrown when an endpoint is called for a section which does not support that
    endpoint.
    """
