import pytest

from onep.onep import main


@pytest.mark.parametrize("option", ("--help", "-h"))
def test_help(capsys, option) -> None:
    main([option])

    output = capsys.readouterr().out

    assert "usage: 1p [-h] [-j] ACCOUNT COMMAND ..." in output
