"""Pruebas de humo: verifica que la base de datos responde y la extension vector existe."""


def test_select_uno(conexion):
    """La conexion esta activa y la BD responde."""
    with conexion.cursor() as cur:
        cur.execute("SELECT 1")
        resultado = cur.fetchone()
    assert resultado == (1,)


def test_extension_vector_existe(conexion):
    """La extension pgvector esta instalada en la base de datos."""
    with conexion.cursor() as cur:
        cur.execute("SELECT extname FROM pg_extension WHERE extname='vector'")
        fila = cur.fetchone()
    assert fila is not None, "La extension 'vector' no esta instalada"
    assert fila[0] == "vector"
