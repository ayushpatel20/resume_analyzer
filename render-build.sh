#!/usr/bin/env bash
# render-build.sh — Build script for Render deployment
set -e

echo "=== AI Resume Analyzer — Render Build ==="

# ── Build React frontend ─────────────────────────────────────────────────────
echo ">>> Building React frontend..."
cd frontend
npm ci --prefer-offline
npm run build
cd ..
echo "✓ Frontend built."

# ── Copy dist into backend/app/dist so FastAPI can serve it ─────────────────
echo ">>> Copying dist to backend/app/dist..."
rm -rf backend/app/dist
cp -r frontend/dist backend/app/dist
echo "✓ Copied."

# ── Create runtime directories ───────────────────────────────────────────────
mkdir -p uploads reports
echo "✓ Runtime dirs ready."

echo "=== Build complete ==="
