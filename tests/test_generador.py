import httpx
import respx

from rag.generador import responder
from rag.modelos import FragmentoRecuperado

FRAGS = [
    FragmentoRecuperado(1, 1, "Doc", "pgvector almacena vectores en Postgres", 0.1),
    FragmentoRecuperado(2, 1, "Doc", "RAG combina recuperacion y generacion", 0.2),
]


def test_extractiva_sin_llm(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    r = responder("que es pgvector", FRAGS)
    assert r.uso_llm is False
    assert "pgvector" in r.texto
    assert r.fuentes == FRAGS


@respx.mock
def test_con_llm(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "x")
    monkeypatch.setenv("LLM_BASE_URL", "https://llm.test/v1")
    cuerpo = {"choices": [{"message": {"content": "pgvector es una extension."}}]}
    ruta = respx.post("https://llm.test/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=cuerpo)
    )
    r = responder("que es pgvector", FRAGS)
    assert ruta.called
    assert r.uso_llm is True
    assert "extension" in r.texto


def test_fallo_llm_cae_a_extractiva(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "x")
    monkeypatch.setenv("LLM_BASE_URL", "https://llm.test/v1")
    with respx.mock:
        respx.post("https://llm.test/v1/chat/completions").mock(return_value=httpx.Response(500))
        r = responder("que es pgvector", FRAGS)
    assert r.uso_llm is False
    assert "pgvector" in r.texto


def test_extractiva_sin_fragmentos(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    r = responder("cualquier cosa", [])
    assert r.uso_llm is False
    assert r.texto  # mensaje de que no hay informacion
