from ..util import run


def share(session, id, time, once):
    args = ["item", "share", id]

    if time is not None:
        args.append(f"--expiry={time}")

    if once:
        args.append("--view-once")

    run(args, session=session)
