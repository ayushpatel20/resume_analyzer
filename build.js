const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('Build script started in:', process.cwd());

const inFrontend = fs.existsSync(path.join(process.cwd(), 'src')) && fs.existsSync(path.join(process.cwd(), 'vite.config.js'));
const hasFrontendDir = fs.existsSync(path.join(process.cwd(), 'frontend'));

if (!inFrontend && hasFrontendDir) {
  console.log('Switching to frontend directory...');
  process.chdir(path.join(process.cwd(), 'frontend'));
}

console.log('Installing dependencies and building Vite bundle...');
execSync('npm install && npm run build', { stdio: 'inherit' });

// Ensure output is available both in ./dist and ../dist / frontend/dist
const distDir = path.join(process.cwd(), 'dist');
const parentDistDir = path.join(process.cwd(), '..', 'dist');

if (fs.existsSync(distDir)) {
  try {
    if (!fs.existsSync(parentDistDir) && path.basename(process.cwd()) === 'frontend') {
      fs.cpSync(distDir, parentDistDir, { recursive: true });
      console.log('Copied dist to root directory for Vercel deployment.');
    }
  } catch (err) {
    console.log('Note: Skipping dist copy (already at root or permissions restricted)');
  }
}

console.log('Build completed successfully.');
