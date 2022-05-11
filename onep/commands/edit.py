from typing import List, Optional

from ..util import fatal, run
from ..fields import Field


def create(
    session: str,
    vault: str,
    title: str,
    url: Optional[str],
    specs: List[str],
    tags: Optional[str],
    length: int,
    symbols: bool,
) -> None:
    fields = list(map(lambda spec: Field.from_spec(spec, length, symbols).to_string(), specs))
    args = ["item", "create", "--category=login", f"--vault={vault}", f"--title={title}"] + fields

    if url is not None:
        args.append(f"--url={url}")

    if tags is not None:
        args.append(f"--tags={tags}")

    (status, _, stderr) = run(args, session=session, silent=True)

    if not status:
        fatal(stderr)
