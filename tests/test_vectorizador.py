import math

import pytest

from rag.vectorizador import DIM, VectorizadorFalso


def test_falso_determinista():
    v = VectorizadorFalso()
    a = v.vectorizar(["hola mundo"])[0]
    b = v.vectorizar(["hola mundo"])[0]
    assert a == b
    assert len(a) == DIM


@pytest.mark.integracion
def test_real_dimension_y_cercania():
    from rag.vectorizador import VectorizadorST

    v = VectorizadorST()
    vs = v.vectorizar(["el perro corre", "el can corre", "tarta de manzana"])
    assert len(vs[0]) == DIM

    def cos(a, b):
        return sum(x * y for x, y in zip(a, b, strict=True)) / (
            math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
        )

    assert cos(vs[0], vs[1]) > cos(vs[0], vs[2])
