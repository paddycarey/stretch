# stdlib imports
import json
import os


def json_fixture(name):
    curdir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(curdir, os.pardir, "fixtures", name + ".json")
    with open(path, 'r') as f:
        fixture = json.loads(f.read())
    return fixture
