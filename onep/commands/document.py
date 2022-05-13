import sys

from typing import Optional

from ..util import fatal, run


def download(session: str, title: str) -> None:
    (status, stdout, stderr) = run(["document", "get", title], session=session, silent=True)

    if not status:
        fatal(stderr)

    print(stdout)


def upload(session: str, vault: str, title: str, file: str, filename: Optional[str]) -> None:
    args = ["document", "create", f"--vault={vault}", f"--title={title}", file]

    if filename is not None:
        args.append(f"--file-name={filename}")

    stdin = None

    if file == "-":
        stdin = sys.stdin.read()

    (status, _, stderr) = run(args, session=session, silent=True, stdin=stdin)

    if not status:
        fatal(stderr)
