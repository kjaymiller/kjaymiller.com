#!/bin/bash
# Quick start script for Content Editor TUI

set -e

# Check if CONNECTION_STRING is already set in environment
if [ -n "$CONNECTION_STRING" ]; then
    echo "Using CONNECTION_STRING from environment"
else
    # If not set, try to load from .env file
    if [ -f .env ]; then
        echo "Loading CONNECTION_STRING from .env"
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "Error: CONNECTION_STRING not set and .env file not found"
        echo "Please either:"
        echo "  1. Set CONNECTION_STRING environment variable, or"
        echo "  2. Create .env file from .env.example:"
        echo ""
        echo "     cp .env.example .env"
        echo "     # Edit .env with your PostgreSQL connection string"
        exit 1
    fi
fi

# Verify CONNECTION_STRING is now set
if [ -z "$CONNECTION_STRING" ]; then
    echo "Error: CONNECTION_STRING is not set"
    exit 1
fi

# Run the app
uv run content-editor
