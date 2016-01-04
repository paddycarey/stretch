# stdlib imports
import logging

# local imports
from stretch import config


def test_get_local_debug(monkeypatch):
    monkeypatch.setenv('LOCAL_DEBUG', 'true')
    assert config.get_local_debug()


def test_get_local_debug_not_set():
    assert not config.get_local_debug()


def test_get_log_level(monkeypatch):
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')
    assert config.get_log_level() == logging.DEBUG


def test_get_log_level_not_set():
    assert config.get_log_level() == logging.INFO


def test_get_log_level_invalid(monkeypatch):
    monkeypatch.setenv('LOG_LEVEL', 'log all the things')
    assert config.get_log_level() == logging.INFO


def test_get_marathon_url(monkeypatch):
    expected = 'http://marathon.example.com'
    monkeypatch.setenv('MARATHON_URL', expected)
    assert config.get_marathon_url() == expected


def test_get_marathon_url_not_set():
    assert config.get_marathon_url() == "http://leader.mesos:8080"


def test_get_sleep_seconds(monkeypatch):
    expected = 60
    monkeypatch.setenv('SLEEP_SECONDS', expected)
    assert config.get_sleep_seconds() == expected


def test_get_sleep_seconds_not_set():
    assert config.get_sleep_seconds() == 30


def test_get_sleep_seconds_not_a_number(monkeypatch):
    monkeypatch.setenv('SLEEP_SECONDS', 'sixty')
    assert config.get_sleep_seconds() == 30
