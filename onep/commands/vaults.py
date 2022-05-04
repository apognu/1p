from ..util import run


def vaults(session: str, json: bool) -> None:
    run(["vault", "list", f"--session={session}"], json=json)


def vault(session: str, json: bool, id: str) -> None:
    run(["vault", "get", id, f"--session={session}"], json=json)
