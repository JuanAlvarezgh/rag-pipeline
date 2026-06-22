from pgvector.utils import Vector

from rag.modelos import FragmentoRecuperado


def guardar_documento(conexion, titulo: str, fuente: str | None = None) -> int:
    with conexion.cursor() as cur:
        cur.execute(
            "INSERT INTO documentos (titulo, fuente) VALUES (%s, %s) RETURNING id",
            (titulo, fuente),
        )
        id_doc = cur.fetchone()[0]
    conexion.commit()
    return id_doc


def guardar_fragmentos(
    conexion,
    id_documento: int,
    textos: list[str],
    vectores: list[list[float]],
) -> None:
    with conexion.cursor() as cur:
        for orden, (texto, vector) in enumerate(zip(textos, vectores, strict=True)):
            cur.execute(
                "INSERT INTO fragmentos (id_documento, orden, texto, vector)"
                " VALUES (%s, %s, %s, %s)",
                (id_documento, orden, texto, Vector(vector)),
            )
    conexion.commit()


def buscar_similares(
    conexion,
    vector: list[float],
    k: int = 4,
) -> list[FragmentoRecuperado]:
    v = Vector(vector)
    with conexion.cursor() as cur:
        cur.execute(
            "SELECT f.id, f.id_documento, d.titulo, f.texto, f.vector <=> %s AS distancia "
            "FROM fragmentos f JOIN documentos d ON d.id = f.id_documento "
            "ORDER BY f.vector <=> %s LIMIT %s",
            (v, v, k),
        )
        filas = cur.fetchall()
    return [
        FragmentoRecuperado(
            id=r[0],
            id_documento=r[1],
            titulo=r[2],
            texto=r[3],
            distancia=float(r[4]),
        )
        for r in filas
    ]
