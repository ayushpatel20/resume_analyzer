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
    const targets = [
      parentDistDir,
      path.join(process.cwd(), '..', 'backend', 'dist'),
      path.join(process.cwd(), '..', 'backend', 'app', 'dist'),
    ];
    for (const target of targets) {
      fs.cpSync(distDir, target, { recursive: true });
    }
    console.log('Mirrored dist to root and backend directories for Vercel deployment.');
  } catch (err) {
    console.log('Note: Skipping dist copy:', err.message);
  }
}


console.log('Build completed successfully.');
