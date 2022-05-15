import pytest
import mock

from onep.onep import main
from . import common


@common.session
@mock.patch("onep.commands.vaults.run", return_value=(False, "", "dummy error from upstream"))
def test_error(a, capsys):
    with pytest.raises(SystemExit) as e:
        main(["personal", "vaults"])

    output = capsys.readouterr().err

    assert e.value.code == 1
    assert "ERROR:" in output
    assert "dummy error from upstream" in output
