# stdlib imports
import re

# third-party imports
import structlog

# local imports
from stretch import exceptions
from stretch import logging
from .trigger_types import http
from .trigger_types import mesos

logger = structlog.get_logger()


class ParseTriggerError(exceptions.StretchException):

    def log_message(self):
        return "Unable to parse trigger configuration"


class InvalidTriggerType(ParseTriggerError):

    def __init__(self, trigger_type):
        super().__init__(trigger_type)
        self.trigger_type = trigger_type

    def log_message(self):
        return "Invalid tigger type: %s" % self.trigger_type


def get_prefixes_from_labels(labels):
    """Extracts a unique list of trigger prefixes from a dict of labels.
    """
    regex = r'^SCALING_TRIGGER_[0-9]+_'
    trigger_prefixes = set()
    for k in labels:
        match = re.match(regex, k)
        if match is not None:
            trigger_prefixes.add(match.group(0))
    return trigger_prefixes


def get_trigger_type_from_string(name):
    """Returns the appropriate trigger type for the given name
    """
    try:
        return {
            "cpu": mesos.CPUTrigger,
            "mem": mesos.MemTrigger,
            "http": http.HttpTrigger,
            "http_single": http.HttpSingleTrigger,
        }[name]
    except KeyError:
        raise InvalidTriggerType(name)


def get_configs_from_labels(prefixes, labels):
    """Transforms a raw "labels" dict of (str, str) pairs into a list of
    dicts, each containing the configuration keys for a single trigger.
    """
    trigger_configs = []
    for trigger_prefix in prefixes:
        trigger_config = {}
        for key, value in labels.items():
            if key.startswith(trigger_prefix):
                trigger_key = key.replace(trigger_prefix, "").lower()
                trigger_config[trigger_key] = value
        trigger_configs.append(trigger_config)
    return trigger_configs


def get_triggers_from_configs(app_id, tasks, configs):
    """Returns an initialised Trigger object for the given configuration
    """
    for config in configs:
        try:
            trigger_type = get_trigger_type_from_string(config.get("type"))
            yield trigger_type(app_id=app_id, tasks=tasks, **config)
        except Exception as e:
            logging.log_exception(e, app_id=app_id)


def parse_triggers(app_id, tasks, labels):
    """Execute the parser and return all configured triggers
    """
    prefixes = get_prefixes_from_labels(labels)
    configs = get_configs_from_labels(prefixes, labels)
    return [t for t in get_triggers_from_configs(app_id, tasks, configs)]
