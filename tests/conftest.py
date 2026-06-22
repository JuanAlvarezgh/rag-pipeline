import os

import psycopg
import pytest
from pgvector.psycopg import register_vector

DSN = os.environ.get("PG_DSN_TEST", "postgresql://rag:rag@localhost:5438/rag")


def _ejecutar_script(cur, ruta):
    for sentencia in open(ruta, encoding="utf-8").read().split(";"):
        if sentencia.strip():
            cur.execute(sentencia)


@pytest.fixture()
def conexion():
    con = psycopg.connect(DSN)
    con.autocommit = True
    with con.cursor() as cur:
        # El seed crea la extension `vector`; debe existir antes de register_vector.
        _ejecutar_script(cur, "seed/01_esquema.sql")
        cur.execute("TRUNCATE fragmentos, documentos RESTART IDENTITY CASCADE")
    register_vector(con)
    yield con
    con.close()
