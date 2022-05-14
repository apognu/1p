import pytest
import mock

from onep.onep import main


@mock.patch("onep.onep.check_session", return_value="dummysession")
@mock.patch("onep.util.load_session", return_value="dummysession")
@mock.patch("onep.commands.vaults.run", return_value=(True, "{}", ""))
def test_no_vaults(a, b, c):
    with pytest.raises(SystemExit) as e:
        main(["personal", "vaults"])

    assert "There are no vaults in this account." in str(e.value)


TWO_VAULTS_OUTPUT = """[{"id": "vault1", "name": "First vault"}, {"id": "vault2", "name": "Second vault"}]"""


@mock.patch("onep.onep.check_session", return_value="dummysession")
@mock.patch("onep.util.load_session", return_value="dummysession")
@mock.patch("onep.commands.vaults.run", return_value=(True, TWO_VAULTS_OUTPUT, ""))
def test_two_vaults(a, b, c, capsys):
    main(["personal", "vaults"])

    output = capsys.readouterr().out

    assert "vault1" in output
    assert "First vault" in output
    assert "vault2" in output
    assert "Second vault" in output
