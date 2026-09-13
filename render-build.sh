#!/usr/bin/env bash
# render-build.sh — Build script for Render deployment
# Runs during the "Build Command" phase on Render

set -e  # Exit on any error

echo "=== AI Resume Analyzer — Render Build Script ==="
echo "Working directory: $(pwd)"

# ── 1. Build React frontend ─────────────────────────────────────────────────
echo ""
echo ">>> Step 1: Building React frontend..."
cd frontend
npm ci --prefer-offline
npm run build
cd ..
echo "✓ Frontend built successfully."

# ── 2. Copy dist into backend so FastAPI can serve it ───────────────────────
echo ""
echo ">>> Step 2: Copying dist/ into backend/app/dist/ ..."
rm -rf backend/app/dist
cp -r frontend/dist backend/app/dist
echo "✓ Frontend assets copied to backend/app/dist"

# ── 3. Install Python dependencies ──────────────────────────────────────────
echo ""
echo ">>> Step 3: Installing Python dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..
echo "✓ Python packages installed."

# ── 4. Create required runtime directories ──────────────────────────────────
echo ""
echo ">>> Step 4: Creating runtime directories..."
mkdir -p uploads reports data
echo "✓ Directories ready."

echo ""
echo "=== Build complete! ==="
