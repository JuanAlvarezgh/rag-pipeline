import hashlib

DIM = 384
_MODELO = "paraphrase-multilingual-MiniLM-L12-v2"


class VectorizadorFalso:
    """Vectorizador determinista para pruebas: mismo texto -> mismo vector."""

    dim = DIM

    def vectorizar(self, textos: list[str]) -> list[list[float]]:
        vectores = []
        for t in textos:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            vec = [((h[i % len(h)] / 255.0) * 2 - 1) for i in range(self.dim)]
            vectores.append(vec)
        return vectores


class VectorizadorST:
    """Vectorizador real con sentence-transformers (modelo multilingue)."""

    dim = DIM

    def __init__(self, modelo: str = _MODELO):
        from sentence_transformers import SentenceTransformer

        self._modelo = SentenceTransformer(modelo)

    def vectorizar(self, textos: list[str]) -> list[list[float]]:
        emb = self._modelo.encode(textos, normalize_embeddings=True)
        return [v.tolist() for v in emb]
