#!/usr/bin/env python
"""stretch. Dead simple autoscaling for Marathon.

See README.md for full configuration instructions.
"""
# stdlib imports
import time

# third-party imports
import structlog

# local imports
from stretch import scaling
from stretch import config
from stretch import logging
from stretch import marathon

logger = structlog.get_logger()


def run_forever(marathon_url, sleep_seconds):
    """Run stretch's fetch/check/scale process repeatedly, sleeping for a
    configurable number of seconds between runs.
    """
    marathon_client = marathon.MarathonClient(marathon_url)
    scaling_client = scaling.ScalingClient(marathon_client)

    while True:
        try:
            apps = scaling_client.list_applications()
        except Exception as e:
            logging.log_exception(e)
            apps = []
        for app in apps:
            try:
                scaling_client.process_application(app)
            except Exception as e:
                logging.log_exception(e, app_id=app.app_id)
        time.sleep(sleep_seconds)


if __name__ == "__main__":

    # configure global logging settings
    log_level = config.get_log_level()
    local_debug = config.get_local_debug()
    logging.configure_logging(log_level, local_debug)

    # grab configuration from the environment
    marathon_url = config.get_marathon_url()
    sleep_seconds = config.get_sleep_seconds()

    # run the autoscaler in an infinite loop
    run_forever(marathon_url, sleep_seconds)
    logger.info("stretch exiting")
