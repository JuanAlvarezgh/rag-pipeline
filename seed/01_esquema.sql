CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documentos (
    id         SERIAL PRIMARY KEY,
    titulo     TEXT NOT NULL,
    fuente     TEXT,
    creado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fragmentos (
    id            BIGSERIAL PRIMARY KEY,
    id_documento  INTEGER NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
    orden         INTEGER NOT NULL,
    texto         TEXT NOT NULL,
    vector        vector(384),
    creado_en     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fragmentos_vector
    ON fragmentos USING hnsw (vector vector_cosine_ops);
