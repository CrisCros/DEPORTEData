#!/usr/bin/env sh
set -eu

if [ -f package.json ]; then
  npm run build
  rm -rf .vercel-dist
  cp -R dist .vercel-dist
elif [ -f frontend/package.json ]; then
  cd frontend
  npm run build
  rm -rf ../.vercel-dist
  cp -R dist ../.vercel-dist
elif [ -f ../frontend/package.json ]; then
  cd ../frontend
  npm run build
  rm -rf ../backend/.vercel-dist
  cp -R dist ../backend/.vercel-dist
else
  echo "No frontend package.json found"
  exit 1
fi
