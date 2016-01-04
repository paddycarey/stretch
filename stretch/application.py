# stdlib imports
import math

# third-party imports
from cached_property import cached_property

# local imports
from .triggers import parser
from .triggers import results


class Application(object):

    def __init__(self, app_json):
        self.app_id = app_json.get('id')
        self.instances = app_json.get('instances')
        self.tasks = app_json.get('tasks')
        self.labels = app_json.get('labels')

    @property
    def max_instances(self):
        return int(self.labels.get("SCALING_MAX_INSTANCES", self.instances))

    @property
    def min_instances(self):
        return int(self.labels.get("SCALING_MIN_INSTANCES", self.instances))

    @property
    def scaling_factor(self):
        return float(self.labels.get("SCALING_FACTOR", 1.5))

    @cached_property
    def new_instances(self):
        return InstanceCalculator(self.instances,
                                  self.min_instances,
                                  self.max_instances,
                                  self.scaling_factor)

    @cached_property
    def triggers(self):
        return parser.parse_triggers(self.app_id, self.tasks, self.labels)

    def autoscaling_enabled(self):
        """Check if autoscaling is enabled by checking if at least one trigger
        is configured.
        """
        return len(self.triggers) > 0

    def check_triggers(self):
        """Check all configured triggers and return all results.
        """
        return [trigger.check() for trigger in self.triggers]

    def validate(self):
        """Validate that all required fields parse correctly from JSON.
        """
        for prop in ['app_id', 'instances', 'tasks', 'labels']:
            if getattr(self, prop) is None:
                return False
        for prop in ['max_instances', 'min_instances', 'scaling_factor']:
            try:
                getattr(self, prop)
            except ValueError:
                return False
        return True


class InstanceCalculator(object):

    def __init__(self, instances, min_instances, max_instances, scaling_factor):
        self.current_instances = instances
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.scaling_factor = scaling_factor

    def _scale_down_instances(self):
        new_instances = int(math.floor(self.current_instances / self.scaling_factor))
        return max(self.min_instances, new_instances)

    def _scale_up_instances(self):
        new_instances = int(math.ceil(self.current_instances * self.scaling_factor))
        return min(self.max_instances, new_instances)

    @property
    def _calculator_funcs(self):
        return {
            results.CheckResults.SCALE_DOWN: self._scale_down_instances,
            results.CheckResults.SCALE_UP: self._scale_up_instances,
        }

    def calculate(self, trigger_result):
        try:
            return self._calculator_funcs[trigger_result]()
        except KeyError:
            return self.current_instances
