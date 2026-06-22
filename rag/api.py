from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag import almacen, generador, recuperador
from rag.bd import conectar
from rag.fragmentador import fragmentar


class CuerpoIngerir(BaseModel):
    titulo: str
    texto: str
    fuente: str | None = None


class CuerpoConsultar(BaseModel):
    pregunta: str
    k: int = 4


def crear_app(vectorizador=None) -> FastAPI:
    if vectorizador is None:
        from rag.vectorizador import VectorizadorST

        vectorizador = VectorizadorST()

    app = FastAPI(
        title="rag-pipeline",
        description="API de RAG: ingesta de documentos y consulta con recuperacion aumentada.",
    )

    @app.get("/salud")
    def salud():
        return {"estado": "ok"}

    @app.post("/ingerir")
    def ingerir(cuerpo: CuerpoIngerir):
        textos = fragmentar(cuerpo.texto)
        if not textos:
            raise HTTPException(status_code=400, detail="El texto esta vacio")
        vectores = vectorizador.vectorizar(textos)
        con = conectar()
        try:
            id_doc = almacen.guardar_documento(con, cuerpo.titulo, cuerpo.fuente)
            almacen.guardar_fragmentos(con, id_doc, textos, vectores)
        finally:
            con.close()
        return {"id_documento": id_doc, "fragmentos": len(textos)}

    @app.post("/consultar")
    def consultar(cuerpo: CuerpoConsultar):
        con = conectar()
        try:
            fragmentos = recuperador.recuperar(con, vectorizador, cuerpo.pregunta, k=cuerpo.k)
        finally:
            con.close()
        resp = generador.responder(cuerpo.pregunta, fragmentos)
        return {
            "respuesta": resp.texto,
            "uso_llm": resp.uso_llm,
            "fuentes": [
                {"texto": f.texto, "titulo": f.titulo, "distancia": f.distancia}
                for f in fragmentos
            ],
        }

    return app
