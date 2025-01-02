# Marimo dev

Create a DevContainer for Marimo.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/marimo_dev)

We follow two strategies here.
An **external** Marimo server fired up at the start using

```json
{"postStartCommand": "uv run marimo --yes edit --host=localhost --port=8080 --headless --no-token"}
```

and an **embedded** (into vscode) server induced by the
***marimo-team.vscode-marimo*** extension.

We use a simple devcontainer.json file

```json
{
    "name": "Python Dev Container",
    "image": "mcr.microsoft.com/devcontainers/python:3.12",
    "hostRequirements": {
        "cpus": 4
    },
    "features": {
        "ghcr.io/devcontainers/features/common-utils:2": {}
    },
    "forwardPorts": [8080],
    "customizations": {
        "vscode": {
            "settings": {
                "python.defaultInterpreterPath": "/workspaces/marimo_dev/.venv/bin/python",
                "python.linting.enabled": true,
                "python.linting.pylintEnabled": true,
                "marimo.pythonPath": "/workspaces/marimo_dev/.venv/bin/python",
                "marimo.marimoPath": "/workspaces/marimo_dev/.venv/bin/marimo"
            },
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "marimo-team.vscode-marimo"
            ]
        }
    },
    "postCreateCommand": "curl -LsSf https://astral.sh/uv/install.sh | sh && . ~/.profile && uv venv && . .venv/bin/activate && uv pip install marimo && uv pip install -r requirements.txt",
    "postStartCommand": "uv run marimo --yes edit --host=localhost --port=8080 --headless --no-token",
    "remoteUser": "vscode"
}
```

We install uv to keep the construction fast and responsive.
