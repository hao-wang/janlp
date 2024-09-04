FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install unidic and download dictionary
RUN pip install unidic && \
    python -m unidic download && \
    mv $(python -c "import unidic; print(unidic.DICDIR)") /app/dicdir

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
  cd /usr/local/bin && \
  ln -s /opt/poetry/bin/poetry && \
  poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

RUN bash -c "poetry install"


COPY ./janlp ./janlp
ENV PYTHONPATH=/app

CMD ["fastapi", "run", "janlp/main.py", "--host", "0.0.0.0", "--port", "8000"]