import pytest
import mock

from onep.onep import main


@mock.patch("onep.onep.check_session", return_value="dummysession")
@mock.patch("onep.util.load_session", return_value="dummysession")
@mock.patch("onep.commands.vaults.run", return_value=(False, "", "dummy error from upstream"))
def test_error(a, b, c, capsys):
    with pytest.raises(SystemExit) as e:
        main(["personal", "vaults"])

    output = capsys.readouterr().err

    assert e.value.code == 1
    assert "ERROR:" in output
    assert "dummy error from upstream" in output
