from typing import Optional
import keyring
import os

from ..util import KEYRING_SERVICE, is_plain_secret_storage, fatal, run, session_file


def signin(account: str) -> Optional[str]:
    (status, stdout, stderr) = run(["signin", "--raw", f"--account={account}"], silent=True)

    if not status:
        fatal(stderr)

    if is_plain_secret_storage():
        try:
            fd = os.open(session_file(account), os.O_CREAT | os.O_WRONLY, 0o600)

            with open(fd, "w") as f:
                f.write(stdout)

            return stdout
        except Exception as e:
            fatal(f"cannot write session file: {type(e).__name__}")
    else:
        try:
            keyring.set_password(KEYRING_SERVICE, account, stdout)

            return stdout
        except keyring.errors.KeyringError as e:
            fatal(f"cannot write session file: {type(e).__name__}")
