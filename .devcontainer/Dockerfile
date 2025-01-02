FROM python:3.12-slim

# Copy UV installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN uv pip install --system --no-cache-dir marimo && \
    mkdir -p /workspace

# Create a non-root user
#ARG USERNAME=vscode
#ARG USER_UID=1000
#ARG USER_GID=$USER_UID

#RUN groupadd --gid $USER_GID $USERNAME \
#    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
#RUN mkdir -p /workspace
    #&& chown -R $USERNAME:$USERNAME /workspace

# Configure Jupyter
WORKDIR /workspace

# Set up entrypoint
EXPOSE 2818
#EXPOSE 3015

#CMD ["marimo", "--yes", "edit", "/workspace/marimo_dev/notebooks", "--host=localhost", "--port=2818", "--headless",  "--no-token"]
