def fragmentar(texto: str, tam: int = 500, solapamiento: int = 80) -> list[str]:
    texto = texto.strip()
    if not texto:
        return []
    if len(texto) <= tam:
        return [texto]
    paso = max(1, tam - solapamiento)
    fragmentos = []
    inicio = 0
    while inicio < len(texto):
        fragmentos.append(texto[inicio : inicio + tam])
        inicio += paso
    return fragmentos
