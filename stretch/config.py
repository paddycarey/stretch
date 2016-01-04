# stdlib imports
import logging
import os

# third-party imports
import structlog

logger = structlog.get_logger()


def get_local_debug():
    """If LOCAL_DEBUG is set, exceptions will be pretty printed to stdout and
    removed from the log messages.

    This is optional, default: not set.
    """
    return os.environ.get("LOCAL_DEBUG") is not None


def get_log_level():
    """Get logging level from the environment.

    This is optional, default: `INFO`.
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    try:
        return {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }[log_level.upper()]
    except KeyError:
        logger.warning("Unable to parse LOG_LEVEL environment variable, using default: INFO")
        return logging.INFO


def get_marathon_url():
    """Get Marathon URL from the environment.

    This is optional, default: http://leader.mesos:8080.
    """
    marathon_url = os.environ.get("MARATHON_URL", None)
    if marathon_url is None:
        logger.warning("Unable to parse MARATHON_URL environment variable, using default: http://leader.mesos:8080")
        marathon_url = "http://leader.mesos:8080"
    return marathon_url


def get_sleep_seconds():
    """Get sleep seconds (the delay between autoscaler runs) from the
    environment.

    This is optional, default: 30.
    """
    sleep_seconds = os.environ.get("SLEEP_SECONDS", 30)
    try:
        sleep_seconds = int(sleep_seconds)
    except ValueError:
        logger.warning("Unable to parse SLEEP_SECONDS environment variable, using default: 30")
        sleep_seconds = 30
    return sleep_seconds
