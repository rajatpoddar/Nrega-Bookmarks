#!/bin/bash

# 1. Project folder me jao (Yahan folder ka naam apne hisaab se check kar lena agar alag ho)
cd /volume1/docker/Projects/nrega-bookmarks/

# --- FIX START ---
# Git permission error fix karne ke liye
git config --global --add safe.directory /volume1/docker/Projects/nrega-bookmarks
# --- FIX END ---

# 2. GitHub se naya code khicho
echo "Pulling latest code from GitHub..."
git pull origin main

# 3. Docker container ko naye code ke sath rebuild karo
echo "Rebuilding Docker container..."
sudo docker-compose up -d --build

echo "Update Complete! 🚀"