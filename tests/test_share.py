import mock
import pytest

from onep.onep import main
from tests import common


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
def test_share(capsys):
    main(["personal", "share", "dummy"])

    output = capsys.readouterr().out

    assert "item share dummy --session=dummysession" in output


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
@pytest.mark.parametrize("option", ("--time", "-t"))
def test_share_expiry(capsys, option):
    main(["personal", "share", "dummy", option, "1h"])

    output = capsys.readouterr().out

    assert "item share dummy --expiry=1h --session=dummysession" in output


@common.session
@mock.patch("onep.util.OP_COMMAND", "echo")
@pytest.mark.parametrize("option", ("--once", "-o"))
def test_share_once(capsys, option):
    main(["personal", "share", "dummy", option])

    output = capsys.readouterr().out

    assert "item share dummy --view-once --session=dummysession" in output
