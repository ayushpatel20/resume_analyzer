const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('Build script started in backend, navigating to frontend...');

const frontendDir = path.resolve(__dirname, '..', 'frontend');
if (fs.existsSync(frontendDir)) {
  process.chdir(frontendDir);
  console.log('Building Vite React frontend...');
  execSync('npm install && npm run build', { stdio: 'inherit' });
  
  const frontendDist = path.join(frontendDir, 'dist');
  const backendDist = path.resolve(__dirname, 'dist');
  const appDist = path.resolve(__dirname, 'app', 'dist');
  if (fs.existsSync(frontendDist)) {
    fs.cpSync(frontendDist, backendDist, { recursive: true });
    fs.cpSync(frontendDist, appDist, { recursive: true });
    console.log('Copied dist to backend/dist and backend/app/dist for Vercel.');
  }

} else {
  console.log('Frontend directory not found at', frontendDir);
}
