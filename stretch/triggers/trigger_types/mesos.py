# third-party imports
import requests

# local imports
from .base import PerTaskTrigger
from .base import ThresholdTrigger


class MesosTrigger(PerTaskTrigger, ThresholdTrigger):

    def get_statistics(self, task):
        """Get current resource usage statistics from Mesos for the given task
        """
        url = 'http://' + task['host'] + ':5051/monitor/statistics.json'
        for task_stats in requests.get(url).json():
            if task_stats['executor_id'] == task['id']:
                return task_stats['statistics']


class CPUTrigger(MesosTrigger):

    def get_current_task_value(self, task):
        """Get total CPU time (system + user) in seconds for the given task
        """
        stats = self.get_statistics(task)
        if stats is None:
            return None
        return stats['cpus_system_time_secs'] + stats['cpus_user_time_secs']


class MemTrigger(MesosTrigger):

    def get_current_task_value(self, task):
        """Get percentage memory utilisation for the given task (in bytes)
        """
        stats = self.get_statistics(task)
        if stats is None:
            return None
        mem_rss_bytes = int(stats['mem_rss_bytes'])
        mem_limit_bytes = int(stats['mem_limit_bytes'])
        return 100 * (float(mem_rss_bytes) / float(mem_limit_bytes))
