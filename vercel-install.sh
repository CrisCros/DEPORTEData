#!/usr/bin/env sh
set -eu

if [ -f package.json ]; then
  npm install
elif [ -f frontend/package.json ]; then
  cd frontend
  npm install
elif [ -f ../frontend/package.json ]; then
  cd ../frontend
  npm install
else
  echo "No frontend package.json found"
  exit 1
fi
