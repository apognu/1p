import functools
from unittest.mock import MagicMock
import mock


def session(func):
    @mock.patch("onep.onep.check_session", mock.MagicMock(return_value="dummysession"))
    @mock.patch("onep.util.load_session", mock.MagicMock(return_value="dummysession"))
    @functools.wraps(func)
    def _func(*args, **kwargs):
        func(*args, **kwargs)

    return _func
