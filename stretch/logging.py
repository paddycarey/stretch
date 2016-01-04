# stdlib imports
import logging
import sys

# third-party imports
import structlog

# local imports
from .exceptions import StretchException

logger = structlog.get_logger()


def configure_logging(level, local_debug=False):
    """Set global logging configuration
    """
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if local_debug:
        processors.append(structlog.processors.ExceptionPrettyPrinter())
    processors.append(structlog.processors.JSONRenderer())
    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(stream=sys.stdout, format='%(message)s', level=level)
    # disable logging from some noisy libraries
    logging.getLogger("requests").setLevel(logging.WARNING)


def _log_generic_exception(exception, **kwargs):
    logger.error("An exception occurred", exc_info=True, **kwargs)


def _log_stretch_exception(exception, **kwargs):
    logger_func = getattr(logger, exception.level)
    logger_func(
        exception.format_message(),
        **dict(exception.kwargs, **kwargs)
    )


def log_exception(exception, **kwargs):
    log_funcs = [_log_generic_exception, _log_stretch_exception]
    log_func = log_funcs[int(isinstance(exception, StretchException))]
    log_func(exception, **kwargs)
