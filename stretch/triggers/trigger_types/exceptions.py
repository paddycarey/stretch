# local imports
from stretch import exceptions


class TriggerError(exceptions.StretchException):
    pass


class TriggerConfigurationError(TriggerError):
    pass
