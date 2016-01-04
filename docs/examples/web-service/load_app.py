# stdlib imports
import datetime
import itertools
import sys
import time

# third-party imports
import requests


def main(marathon_api):
    while True:
        try:
            url = "%s/v2/apps/stretch-example-web-service?embed=app.tasks" % marathon_api
            app = requests.get(url).json()['app']
        except:
            print "FAIL list"
            time.sleep(1)
            continue
        urls = itertools.cycle(['http://{0}:{1}'.format(x['host'], x['ports'][0]) for x in app['tasks']])

        x = 0
        while x < 1000:
            try:
                requests.get(urls.next())
                print datetime.datetime.utcnow().isoformat()
            except:
                print "FAIL load"
                time.sleep(1)
                break
            x += 1


if __name__ == "__main__":

    marathon_api = sys.argv[1]
    main(marathon_api)
