import os

import httpx

from rag.modelos import Respuesta


def _extractiva(fragmentos) -> str:
    if not fragmentos:
        return "No se encontro informacion relevante en el corpus."
    lineas = ["Segun los fragmentos mas relevantes del corpus:"]
    for f in fragmentos:
        lineas.append(f"- {f.texto}")
    return "\n".join(lineas)


def _llamar_llm(pregunta: str, contexto: str, api_key: str, base_url: str, modelo: str) -> str:
    mensajes = [
        {"role": "system", "content": "Responde en espanol usando solo el contexto dado."},
        {"role": "user", "content": f"Contexto:\n{contexto}\n\nPregunta: {pregunta}"},
    ]
    resp = httpx.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": modelo, "messages": mensajes, "temperature": 0.2},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def responder(pregunta: str, fragmentos) -> Respuesta:
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        return Respuesta(texto=_extractiva(fragmentos), fuentes=fragmentos, uso_llm=False)
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    modelo = os.environ.get("LLM_MODELO", "gpt-4o-mini")
    contexto = "\n\n".join(f.texto for f in fragmentos)
    try:
        texto = _llamar_llm(pregunta, contexto, api_key, base_url, modelo)
        return Respuesta(texto=texto, fuentes=fragmentos, uso_llm=True)
    except Exception:  # noqa: BLE001
        return Respuesta(texto=_extractiva(fragmentos), fuentes=fragmentos, uso_llm=False)
