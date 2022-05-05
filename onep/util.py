from typing import Optional, List, Tuple
import keyring
import os
import subprocess
import sys

from os import path

from .colors import *

CACHE_DIR = path.expanduser("~/.cache/1p")
KEYRING_SERVICE = "com.github.apognu.1p"


def exit(message: str) -> None:
    print(message.strip(), file=sys.stdout)
    sys.exit(0)


def fatal(message: str) -> None:
    print(f"{red('ERROR:')} {message.strip()}", file=sys.stdout)
    sys.exit(1)


def run(args: List[str], session: Optional[str] = None, json: bool = False, silent: bool = False) -> Tuple[bool, str, str]:
    if session is not None:
        args.append(f"--session={session}")

    if json:
        args.append("--format=json")

    cmd = subprocess.Popen(["op"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = cmd.communicate()

    if not silent:
        if len(stdout) > 0:
            print(stdout.decode("utf-8").strip())

        if len(stderr) > 0:
            print(stderr.decode("utf-8").strip())

    return (cmd.returncode == 0, stdout.decode("utf-8"), stderr.decode("utf-8"))


def is_plain_secret_storage() -> bool:
    return os.getenv("ONEP_SECRET_BACKEND") == "plain"


def init_secret_storage() -> None:
    if is_plain_secret_storage():
        if not path.isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR, mode=0o700)

        if oct(os.stat(CACHE_DIR).st_mode & 0o777) != oct(0o700):
            fatal("cannot use session directory because mode is not 700")


def session_file(account: str) -> str:
    return path.join(CACHE_DIR, f"{account}.token")


def load_session(account: str) -> Optional[str]:
    if is_plain_secret_storage():
        try:
            file = session_file(account)

            if oct(os.stat(file).st_mode & 0o777) != oct(0o600):
                fatal("cannot use session because mode is not 600")

            with open(file) as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            fatal(f"cannot read session file: {type(e).__name__}")
    else:
        try:
            return keyring.get_password(KEYRING_SERVICE, account)
        except keyring.errors.KeyringError as e:
            fatal(f"cannot read session file: {type(e).__name__}")


def check_session(account: str) -> Optional[str]:
    from onep.commands import signin

    session = load_session(account)

    if session is None:
        return signin(account)

    (status, _, _) = run(["account", "get"], session=session, silent=True)

    if not status:
        return signin(account)

    return session
