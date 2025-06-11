#!/bin/bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uvx marimo run --sandbox notebooks/minimal_enclosing_circle.py
