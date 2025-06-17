#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

RAW_DIR="./raw_data"
if [ ! -d "$RAW_DIR" ]; then
  echo "Creating directory: $RAW_DIR"
  mkdir -p "$RAW_DIR"
else
  echo "Directory already exists: $RAW_DIR"
fi

echo "Starting Docker Compose services..."
docker compose up -d