FROM python:3.12-slim

# Build arguments for flexibility
ARG port=8080
ARG username=marimo
ARG user_uid=1000
ARG user_gid=1000

# Labels for metadata
LABEL maintainer="Thomas Schmelzer <thomas.schmelzer@gmail.com>"
LABEL description="Marimo notebook environment with Git support"

# Set environment variables
ENV PORT=${port} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN groupadd --gid ${user_gid} ${username} && \
    useradd --uid ${user_uid} --gid ${user_gid} -m ${username} && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify git installation
RUN git --version

# Set up workspace
WORKDIR /workspaces
RUN chown ${username}:${username} /workspaces

# Copy UV installer and install packages
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

#RUN uv venv && \
#    uv pip install --no-cache-dir marimo==${marimo_version}

# Switch to non-root user
USER ${username}

#RUN uv venv && \
#    uv pip install --no-cache-dir marimo==${marimo_version}

# Expose port
EXPOSE ${PORT}

# Use tini as init process
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command to run marimo
# CMD ["marimo", "edit", "--port", "${PORT}", "--host", "0.0.0.0"]
