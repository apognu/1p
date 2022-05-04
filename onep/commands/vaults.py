from ..util import run


def vaults(session, json):
    run(["vault", "list", f"--session={session}"], json=json)


def vault(session, json, id):
    run(["vault", "get", id, f"--session={session}"], json=json)
