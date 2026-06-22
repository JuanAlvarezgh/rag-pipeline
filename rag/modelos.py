from dataclasses import dataclass, field


@dataclass
class FragmentoRecuperado:
    id: int
    id_documento: int
    titulo: str
    texto: str
    distancia: float


@dataclass
class Respuesta:
    texto: str
    fuentes: list = field(default_factory=list)
    uso_llm: bool = False
