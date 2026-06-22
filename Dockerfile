FROM python:3.11-slim-bookworm
WORKDIR /app
COPY requirements.txt requirements-modelo.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements-modelo.txt
COPY . .
RUN pip install --no-cache-dir -e .
CMD ["uvicorn", "rag.api:crear_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
