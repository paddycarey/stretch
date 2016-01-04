# stdlib imports
from enum import Enum


class CheckResults(Enum):
    """CheckResults containins all possible trigger result states.
    """
    SCALE_DOWN = 0
    DONT_SCALE = 1
    SCALE_UP = 2
    FAILED = 3


def check_results(results):
    """Examines a list of individual check results and returns an overall
    result for all checks combined.
    """
    if CheckResults.SCALE_UP in results:
        return CheckResults.SCALE_UP
    if all(r == CheckResults.SCALE_DOWN for r in results):
        return CheckResults.SCALE_DOWN
    return CheckResults.DONT_SCALE
