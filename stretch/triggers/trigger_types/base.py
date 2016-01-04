# local imports
from .exceptions import TriggerConfigurationError
from stretch.logging import log_exception
from stretch.triggers.results import CheckResults


class BaseTrigger(object):

    def __init__(self, **kwargs):
        self.app_id = kwargs.get('app_id')
        self.trigger_type = kwargs.get('type')
        self.tasks = kwargs.get('tasks')

    def check(self):
        """Subclasses should implement the check() method and it should return
        a stretch.triggers.results.CheckResults value.
        """
        raise NotImplementedError


class ThresholdTrigger(BaseTrigger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lower_threshold = kwargs.get('lower_threshold')
        self._upper_threshold = kwargs.get('upper_threshold')

    @property
    def lower_threshold(self):
        try:
            return float(self._lower_threshold)
        except ValueError:
            raise TriggerConfigurationError(
                "LOWER_THRESHOLD value is not a number",
                value=self._lower_threshold,
            )

    @property
    def upper_threshold(self):
        try:
            return float(self._upper_threshold)
        except ValueError:
            raise TriggerConfigurationError(
                "UPPER_THRESHOLD value is not a number",
                value=self._upper_threshold,
            )

    def check(self):
        """Fetch the current value and compare it to the configured
        upper/lower thresholds, returning results state to the caller.
        """
        try:
            current_value = self.get_current_value()
        except Exception as e:
            log_exception(e, app_id=self.app_id)
            return CheckResults.FAILED
        if current_value >= self.upper_threshold:
            return CheckResults.SCALE_UP
        elif current_value < self.lower_threshold:
            return CheckResults.SCALE_DOWN
        return CheckResults.DONT_SCALE

    def get_current_value(self):
        """Subclasses should implement get_current_value and it should return
        a single float value.
        """
        raise NotImplementedError


class PerTaskTrigger(object):

    def get_current_value(self):
        """Default implementation of get_current_value retrieves an individual
        metric for each running task and averages the value before returning
        to the caller.
        """
        total_value = 0
        for task in self.tasks:
            total_value += self.get_current_task_value(task)
        return total_value / len(self.tasks)

    def get_current_task_value(self, task):
        """Concrete trigger implementations should (most of the time) override
        this method.
        """
        raise NotImplementedError
