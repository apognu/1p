import json
import sys

from typing import List, Optional

from ..util import fatal, run
from ..fields import Field
from ..colors import *


def create(
    session: str,
    vault: str,
    category: str,
    title: str,
    specs: List[str],
    tags: Optional[str],
    length: int,
    symbols: bool,
) -> None:
    fields = list(map(lambda spec: Field.from_spec(spec, length, symbols).to_string(), specs))
    args = ["item", "create", f"--category={category}", f"--vault={vault}", f"--title={title}"] + fields

    if tags is not None:
        args.append(f"--tags={tags}")

    (status, _, stderr) = run(args, session=session, silent=True)

    if not status:
        fatal(stderr)


def edit(
    session: str,
    id: str,
    specs: List[str],
    tags: Optional[str],
    delete: Optional[List[str]],
    length: int,
    symbols: bool,
) -> None:
    fields = list(map(lambda spec: Field.from_spec(spec, length, symbols).to_string(), specs))

    if delete is not None:
        for field in delete:
            fields.append(f"{field}[delete]")

    args = ["item", "edit", id] + fields

    if tags is not None:
        args.append(f"--tags={tags}")

    (status, _, stderr) = run(args, session=session, silent=True)

    if not status:
        fatal(stderr)
