# Marimo dev

Create a DevContainer for Marimo.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/marimo_dev)

We are currently using a simple [devcontainer.json](.devcontainer/devcontainer.json)
file where we install uv to keep the construction fast and responsive.

To set up a DevContainer for Marimo, we offer two strategies:
an **external** Marimo server and an **embedded** server
triggered by the [marimo-team.vscode-marimo](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo) extension.

Let's break down how you can create the DevContainer configuration
step-by-step.

## A tale of two servers

We support both but prefer the external marimo server.

### External Marimo Server

This is started using a postStartCommand
that runs Marimo in the headless mode.

### Embedded Marimo Server

This uses the VS Code extension marimo-team.vscode-marimo
to run Marimo from within the VS Code environment.

## Steps for Creating the DevContainer

### Create the DevContainer Configuration

You'll create a .devcontainer/devcontainer.json file.
This file will configure your container's environment and specify
the necessary commands to run your external Marimo server.
We'll install uv and any dependencies required for
running Marimo inside the container.

Example devcontainer.json

```json
{
    "name": "Marimo Dev Container",
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
    "onCreateCommand": ".devcontainer/startup.sh",
    "postStartCommand": "uv run marimo --yes edit --host=localhost --port=8080 --headless --no-token",
    "remoteUser": "vscode"
}
```

### Breakdown of the Configuration

#### Base Image

We're using a base image for the dev container (mcr.microsoft.com/devcontainers/python:3.12),
but you can replace it with a custom image if needed.

#### VSCode Extensions

marimo-team.vscode-marimo: This extension integrates Marimo with VS Code, allowing you to trigger an embedded server when needed.
ms-python.python: This extension provides Python support and is useful when working with uv.

#### On Create Command

Installs uv after the container is created.
This ensures the required dependencies are in place
before you start the Marimo server.
You may want to adjust the script for your needs.

#### Post Start Command

This command starts the external Marimo server using uv.
The --headless flag ensures that the server runs without
the GUI, and --no-token avoids authentication.

## Working with a configuration

Once the devcontainer.json is set up,
you can open the project in GitHub Codespaces or
use the DevContainer in local VS Code. The steps are as follows:

- Push the configuration to your repository.
- Open the repository in GitHub Codespaces or VSCode with the DevContainer.
- The Marimo server will be started automatically in the background by the postStartCommand.
You can move between VS Code and this server back and forth.

- VS Code Embedded Server
Ensure the marimo-team.vscode-marimo extension is installed in the DevContainer.
You can toggle the embedded server using the extension's command palette
options or configure it to start automatically upon workspace open.

This setup allows you to work both with an external Marimo server and an embedded one,
depending on the mode you're in, and provides an
integrated environment for working with Marimo in VS Code.

## Last but not least

Add a button to your repo's README file

```bash
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/marimo_dev)
```
