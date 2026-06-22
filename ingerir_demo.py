"""Carga el corpus de demostracion en el almacen vectorial."""
import json

from rag import almacen
from rag.bd import conectar
from rag.fragmentador import fragmentar
from rag.vectorizador import VectorizadorST


def main():
    con = conectar()
    with con.cursor() as cur:
        cur.execute("TRUNCATE fragmentos, documentos RESTART IDENTITY CASCADE")
    con.commit()
    vectorizador = VectorizadorST()
    corpus = json.load(open("datos/corpus.json", encoding="utf-8"))
    total_fragmentos = 0
    for doc in corpus:
        textos = fragmentar(doc["texto"])
        vectores = vectorizador.vectorizar(textos)
        id_doc = almacen.guardar_documento(con, doc["titulo"], doc.get("fuente"))
        almacen.guardar_fragmentos(con, id_doc, textos, vectores)
        total_fragmentos += len(textos)
    con.close()
    print(f"Cargados {len(corpus)} documentos y {total_fragmentos} fragmentos.")


if __name__ == "__main__":
    main()
