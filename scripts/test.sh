#!/usr/bin/env bash
set -euo pipefail

export PYSPARK_SUBMIT_ARGS="--driver-memory 2g pyspark-shell"

python -m pytest -v "$@"