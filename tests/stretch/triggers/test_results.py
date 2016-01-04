# local imports
from stretch.triggers.results import check_results
from stretch.triggers.results import CheckResults


def test_check_results_scale_down_one():
    r = [CheckResults.SCALE_DOWN, CheckResults.SCALE_UP, CheckResults.SCALE_UP]
    assert check_results(r) == CheckResults.SCALE_UP


def test_check_results_scale_down_all():
    r = [CheckResults.SCALE_DOWN, CheckResults.SCALE_DOWN, CheckResults.SCALE_DOWN]
    assert check_results(r) == CheckResults.SCALE_DOWN


def test_check_results_scale_up_one():
    r = [CheckResults.SCALE_UP, CheckResults.SCALE_DOWN, CheckResults.SCALE_DOWN]
    assert check_results(r) == CheckResults.SCALE_UP


def test_check_results_scale_up_all():
    r = [CheckResults.SCALE_UP, CheckResults.SCALE_UP, CheckResults.SCALE_UP]
    assert check_results(r) == CheckResults.SCALE_UP


def test_check_results_failed():
    r = [CheckResults.FAILED, CheckResults.SCALE_DOWN, CheckResults.SCALE_DOWN]
    assert check_results(r) == CheckResults.DONT_SCALE


def test_check_results_dont_scale():
    r = [CheckResults.DONT_SCALE, CheckResults.SCALE_DOWN, CheckResults.SCALE_DOWN]
    assert check_results(r) == CheckResults.DONT_SCALE
