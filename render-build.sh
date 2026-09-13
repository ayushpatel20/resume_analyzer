#!/usr/bin/env bash
# render-build.sh — Build script for Render deployment
set -e

echo "=== AI Resume Analyzer — Render Build ==="

# 1. Install Python dependencies
echo ">>> Installing Python requirements..."
pip install -r requirements.txt

# 2. Check if pre-built frontend dist exists; if missing, build React app
if [ ! -f "backend/app/dist/index.html" ]; then
  echo ">>> Pre-built frontend not found. Building React app..."
  cd frontend
  npm install --include=dev
  npm run build
  cd ..
  mkdir -p backend/app/dist
  cp -r frontend/dist/* backend/app/dist/
else
  echo "✓ Pre-built frontend found in backend/app/dist."
fi

# 3. Create runtime directories
mkdir -p uploads reports
echo "✓ Runtime directories ready."

echo "=== Build complete ==="
