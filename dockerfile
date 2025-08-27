FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"
ADD  https://astral.sh/uv/install.sh /uv-installer.sh

RUN apt-get update && \
    apt-get install -y curl && \
    sh /uv-installer.sh && \
    rm /uv-installer.sh && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/list/*

WORKDIR /app

COPY pyproject.toml ./

RUN uv venv
RUN uv sync

COPY main.py ./

EXPOSE 8000


CMD [".venv/bin/fastapi", "run", "main.py", "--host", "0.0.0.0"]