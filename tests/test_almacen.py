from rag import almacen
from rag.vectorizador import VectorizadorFalso

V = VectorizadorFalso()


def test_guardar_y_buscar(conexion):
    id_doc = almacen.guardar_documento(conexion, "Doc 1", "demo")
    textos = [
        "los gatos duermen mucho",
        "el clima esta soleado",
        "las bases de datos guardan datos",
    ]
    vectores = V.vectorizar(textos)
    almacen.guardar_fragmentos(conexion, id_doc, textos, vectores)
    consulta = V.vectorizar(["las bases de datos guardan datos"])[0]
    res = almacen.buscar_similares(conexion, consulta, k=2)
    assert len(res) == 2
    assert res[0].texto == "las bases de datos guardan datos"
    assert res[0].distancia <= res[1].distancia
