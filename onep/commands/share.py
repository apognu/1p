from ..util import run


def share(session: str, id: str, time: str, once: bool) -> None:
    args = ["item", "share", id]

    if time is not None:
        args.append(f"--expiry={time}")

    if once:
        args.append("--view-once")

    run(args, session=session)
