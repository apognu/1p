import json

from ..util import fatal, run


def delete(session: str, archive: bool, id: str) -> None:
    (status, _, stderr) = run(["item", "get", "--format=json", id], session=session, silent=True)

    if not status:
        fatal(stderr)

    args = ["item", "delete", id]

    if archive:
        args.append("--archive")

    (status, _, stderr) = run(args, session=session, silent=True)

    if not status:
        fatal(stderr)
