# third-party imports
import requests

# local imports
from .base import PerTaskTrigger
from .base import ThresholdTrigger
from .exceptions import TriggerError


class RemoteValueError(TriggerError):
    pass


class HttpSingleTrigger(ThresholdTrigger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = kwargs.get('url')

    def get_remote_value(self, url):
        """Fetch a remote URL and parse the result as a float.

        If the endpoint returns something which Python can't parse as a float
        an exception will be raised and this trigger will be marked as having
        failed.
        """
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise RemoteValueError("Unable to fetch remote URL", url=url)

        if response.status_code >= 400 and response.status_code < 600:
            raise RemoteValueError("Remote URL did not return an OK status",
                                   status_code=response.status_code,
                                   url=url)

        try:
            return float(response.text)
        except ValueError:
            raise RemoteValueError("Remote value is not a number",
                                   url=url,
                                   value=response.text)

    def get_current_value(self):
        """Retrieve application-defined value from the given URL (via HTTP)
        """
        return self.get_remote_value(self.url)


class HttpTrigger(PerTaskTrigger, HttpSingleTrigger):

    def get_current_task_value(self, task):
        """Retrieve application-defined value from the given task (via HTTP)
        """
        url = 'http://{0}:{1}/{2}'.format(task['host'],
                                          task['ports'][0],
                                          self.url.lstrip('/'))
        return self.get_remote_value(url)
