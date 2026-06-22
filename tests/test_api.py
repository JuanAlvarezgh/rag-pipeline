import os

from fastapi.testclient import TestClient

from rag.api import crear_app
from rag.vectorizador import VectorizadorFalso

DSN = os.environ.get("PG_DSN_TEST", "postgresql://rag:rag@localhost:5438/rag")


def test_salud():
    cliente = TestClient(crear_app(vectorizador=VectorizadorFalso()))
    assert cliente.get("/salud").json() == {"estado": "ok"}


def test_flujo_ingerir_y_consultar(conexion, monkeypatch):
    monkeypatch.setenv("PG_DSN", DSN)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    cliente = TestClient(crear_app(vectorizador=VectorizadorFalso()))
    r = cliente.post(
        "/ingerir",
        json={
            "titulo": "Doc",
            "texto": "pgvector guarda vectores. RAG recupera y genera.",
            "fuente": "demo",
        },
    )
    assert r.status_code == 200
    assert r.json()["fragmentos"] >= 1
    c = cliente.post(
        "/consultar",
        json={"pregunta": "pgvector guarda vectores. RAG recupera y genera.", "k": 1},
    )
    cuerpo = c.json()
    assert "respuesta" in cuerpo
    assert cuerpo["uso_llm"] is False
    assert len(cuerpo["fuentes"]) == 1


def test_ingerir_texto_vacio_da_400(conexion, monkeypatch):
    monkeypatch.setenv("PG_DSN", DSN)
    cliente = TestClient(crear_app(vectorizador=VectorizadorFalso()))
    r = cliente.post("/ingerir", json={"titulo": "Doc", "texto": "   "})
    assert r.status_code == 400
