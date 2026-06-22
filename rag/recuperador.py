from rag import almacen
from rag.modelos import FragmentoRecuperado


def recuperar(
    conexion,
    vectorizador,
    pregunta: str,
    k: int = 4,
) -> list[FragmentoRecuperado]:
    vector = vectorizador.vectorizar([pregunta])[0]
    return almacen.buscar_similares(conexion, vector, k=k)
