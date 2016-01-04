# third-party imports
import structlog

# local imports
from .application import Application
from .triggers import results

logger = structlog.get_logger()


class ScalingClient(object):

    def __init__(self, marathon_client):
        self.client = marathon_client

    def list_applications(self):
        """Fetch a list of all applications from marathon and filter out those
        that aren't configured for autoscaling.
        """
        apps = [Application(app) for app in self.client.list_applications()]
        apps = [app for app in apps if app.validate()]
        return [app for app in apps if app.autoscaling_enabled()]

    def process_application(self, app):
        """Check an application's triggers and if necessary initiate scaling.
        """
        # check all of an applications configured triggers and return a
        # single result we can use to make a scaling decision.
        trigger_result = results.check_results(app.check_triggers())
        # given the returned tigger_result, calculate the new number of
        # instances that the application should be running.
        new_instances = app.new_instances.calculate(trigger_result)
        # scale the application if required, if not then return None
        if app.instances == new_instances:
            return None

        self.client.scale_application(app.app_id, new_instances)
        logger.info("Scaled application", app_id=app.app_id, new_instances=new_instances)
