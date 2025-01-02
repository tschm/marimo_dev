FROM python:3.12-slim

# Copy UV installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN uv pip install --system --no-cache-dir marimo && \
    mkdir -p /workspace

# Configure Jupyter
WORKDIR /workspace

# Set up entrypoint
EXPOSE 2818
