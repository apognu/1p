import pytest
import mock

from onep.onep import main
from onep.util import exit, fatal
from tests import common


@common.session
@mock.patch("onep.commands.vaults.run", mock.MagicMock(return_value=(False, "", "dummy error from upstream")))
def test_error(capsys):
    with pytest.raises(SystemExit) as e:
        main(["personal", "vaults"])

    output = capsys.readouterr().err

    assert e.value.code == 1
    assert "ERROR:" in output
    assert "dummy error from upstream" in output


def test_fatal(capsys):
    with pytest.raises(SystemExit) as e:
        fatal("dummy error")

    output = capsys.readouterr().err

    assert e.value.code == 1
    assert "ERROR:" in output
    assert "dummy error" in output


def test_exit(capsys):
    with pytest.raises(SystemExit) as e:
        exit("dummy output")

    output = capsys.readouterr().err

    assert e.value.code == 0
    assert "ERROR:" not in output
    assert "dummy output" in output
