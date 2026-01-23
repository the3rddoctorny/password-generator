#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Create venv if missing
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in .venv..."
  python3 -m venv .venv
fi

# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip
python3 -m pip install -U pip >/dev/null

# Install deps if needed
if [ -f "requirements.txt" ]; then
  python3 -m pip install -r requirements.txt >/dev/null
else
  python3 -m pip install pytest selenium axe-selenium-python >/dev/null
fi

echo "Activated venv: $(which python3)"
echo "Python: $(python3 -V)"
echo "Run tests with: python3 -m pytest"

