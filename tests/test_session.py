from tabnanny import check
import mock

from onep.util import load_session, check_session


@mock.patch("keyring.get_password", mock.MagicMock(return_value="dummysession"))
def test_load_session():
    session = load_session("personal")

    assert session == "dummysession"


@mock.patch("keyring.get_password", mock.MagicMock(return_value="dummysession"))
@mock.patch("onep.util.run", mock.MagicMock(return_value=(True, "", "")))
def test_check_session_ok():
    session = check_session("personal")

    assert session == "dummysession"
