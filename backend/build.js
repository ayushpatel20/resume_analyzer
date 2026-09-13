const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('Build script started in backend, navigating to frontend...');

const frontendDir = path.resolve(__dirname, '..', 'frontend');
if (fs.existsSync(frontendDir)) {
  process.chdir(frontendDir);
  console.log('Building Vite React frontend...');
  execSync('npm install && npm run build', { stdio: 'inherit' });
  
  // Copy dist to backend/dist so Vercel can find the output if root is backend
  const frontendDist = path.join(frontendDir, 'dist');
  const backendDist = path.resolve(__dirname, 'dist');
  if (fs.existsSync(frontendDist)) {
    fs.cpSync(frontendDist, backendDist, { recursive: true });
    console.log('Copied dist to backend/dist for Vercel.');
  }
} else {
  console.log('Frontend directory not found at', frontendDir);
}
