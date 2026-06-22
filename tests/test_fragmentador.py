from rag.fragmentador import fragmentar


def test_fragmenta_con_solapamiento():
    texto = "abcdefghij" * 10  # 100 chars
    fragmentos = fragmentar(texto, tam=40, solapamiento=10)
    assert len(fragmentos) >= 3
    assert all(len(f) <= 40 for f in fragmentos)


def test_texto_corto_un_fragmento():
    assert fragmentar("hola", tam=500, solapamiento=50) == ["hola"]


def test_texto_vacio_sin_fragmentos():
    assert fragmentar("", tam=500, solapamiento=50) == []
