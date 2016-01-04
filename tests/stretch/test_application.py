# third-party imports
import pytest

# local imports
from stretch import application
from stretch.triggers import results
from tests.utils import fixture_loader


@pytest.fixture
def configured_app():
    app_json = fixture_loader.json_fixture("web-service-configured")
    return application.Application(app_json)


@pytest.mark.parametrize("property_name,expected", [
    ("app_id", "/web-service"),
    ("instances", 2),
    ("min_instances", 2),
    ("max_instances", 8),
    ("scaling_factor", 1.5),
])
def test_application_parsing(configured_app, property_name, expected):
    assert getattr(configured_app, property_name) == expected


def test_application_parsing_autoscaling_enabled(configured_app):
    assert configured_app.autoscaling_enabled()


def test_application_parsing_new_instances(configured_app):
    assert isinstance(configured_app.new_instances, application.InstanceCalculator)


def test_application_parsing_validate(configured_app):
    assert configured_app.validate()


@pytest.mark.parametrize("instances,min_instances,max_instances,scaling_factor,scaled_up,scaled_down", [
    (0, 0, 8, 1.5, 1, 0),
    (1, 2, 8, 1.5, 2, 2),
    (2, 2, 8, 1.5, 3, 2),
    (3, 2, 8, 1.5, 5, 2),
    (5, 2, 8, 1.5, 8, 3),
    (8, 2, 8, 1.5, 8, 5),
    (10, 2, 8, 1.5, 8, 6),
    (100, 2, 8, 1.5, 8, 8),
    (4, 1, 10, 1.5, 6, 2),
])
def test_instance_calculator_scale_up(instances, min_instances, max_instances,
                                      scaling_factor, scaled_up, scaled_down):
    calc = application.InstanceCalculator(instances,
                                          min_instances,
                                          max_instances,
                                          scaling_factor)
    assert calc.calculate(results.CheckResults.SCALE_UP) == scaled_up
    assert calc.calculate(results.CheckResults.SCALE_DOWN) == scaled_down


def test_instance_calculator_invalid_result_type():
    calc = application.InstanceCalculator(3, 2, 10, 1.5)
    assert calc.calculate(results.CheckResults.DONT_SCALE) == 3
    assert calc.calculate(results.CheckResults.FAILED) == 3
