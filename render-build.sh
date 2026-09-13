#!/usr/bin/env bash
# render-build.sh — Build script for Render deployment
set -e

echo "=== AI Resume Analyzer — Render Build ==="
echo "Node: $(node --version), npm: $(npm --version)"

# ── Build React frontend ─────────────────────────────────────────────────────
echo ">>> Installing frontend dependencies..."
cd frontend
npm install
echo ">>> Building React app..."
npm run build
cd ..
echo "✓ Frontend built."

# ── Copy dist into backend/app/dist so FastAPI can serve it ─────────────────
echo ">>> Copying dist to backend/app/dist..."
rm -rf backend/app/dist
cp -r frontend/dist backend/app/dist
echo "✓ Copied to backend/app/dist"

# ── Create runtime directories ───────────────────────────────────────────────
mkdir -p uploads reports
echo "✓ Runtime dirs ready."

echo "=== Build complete ==="
