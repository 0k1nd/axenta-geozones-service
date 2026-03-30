FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    ca-certificates \
    netcat-traditional \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked

COPY . .

RUN sed -i 's/\r$//' docker/entrypoint.sh \
    && sed -i 's/\r$//' docker/cmd_start_web.sh \
    && chmod +x docker/entrypoint.sh \
               docker/cmd_start_web.sh

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["/app/docker/cmd_start_web.sh"]
