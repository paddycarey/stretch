# third-party imports
import requests

# local imports
from .exceptions import StretchException


class MarathonError(StretchException):
    pass


class DeploymentError(MarathonError):
    pass


class DeploymentInProgress(DeploymentError):
    level = 'debug'


class MarathonClient(object):
    """Marathon HTTP client
    """

    def __init__(self, marathon_url):
        self.marathon_url = marathon_url

    def _make_request(self, method, path, **kwargs):
        request = getattr(requests, method.lower())
        url = self.marathon_url.rstrip("/") + path
        try:
            return request(url, **kwargs)
        except requests.exceptions.ConnectionError:
            raise MarathonError("Unable to connect to marathon endpoint", url=url)

    def list_applications(self):
        """Return a list of all applications currently deployed to marathon.
        """
        params = {"embed": "apps.tasks"}
        response = self._make_request('GET', "/v2/apps", params=params)

        if not response.status_code == 200:
            raise MarathonError("Unable to list applications",
                                status=response.status_code,
                                response=response.text)
        return response.json()['apps']

    def scale_application(self, application_id, instances):
        """Deploys the given application to Marathon.
        """
        path = "/v2/apps/" + application_id.lstrip("/")
        response = self._make_request('PUT', path, json={"instances": instances})

        # 409s are a special case in that they're not really an error, we just
        # sleep and try again next time silently.
        if response.status_code == 409:
            deployment_ids = [x.get('id', 'unknown-id') for x in response.json().get('deployments', [])]
            raise DeploymentInProgress("Unable to scale application",
                                       app_id=application_id,
                                       reason="Deployments in progress: %s" % ','.join(deployment_ids))

        # Other kinds of non-200 responses should be logged as errors as expected.
        if not response.status_code == 200:
            reason = response.json().get('message', 'Unknown. Status: %d' % response.status_code)
            raise DeploymentError("Unable to scale application",
                                  app_id=application_id,
                                  reason=reason)
        return response.json()
