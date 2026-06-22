import os
import time

import psycopg
from pgvector.psycopg import register_vector


def conectar(dsn: str | None = None, reintentos: int = 5, espera: float = 2.0):
    dsn = dsn or os.environ["PG_DSN"]
    ultimo = None
    for _ in range(reintentos):
        try:
            con = psycopg.connect(dsn)
            register_vector(con)
            return con
        except psycopg.OperationalError as e:
            ultimo = e
            time.sleep(espera)
    raise ultimo
