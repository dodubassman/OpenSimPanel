class OpenSimPanelException(Exception):
    pass


class XPlaneIpNotFound(OpenSimPanelException):
    args = "Could not find any running XPlane instance in network."


class XPlaneTimeout(OpenSimPanelException):
    args = "XPlane timeout."
