#!/bin/bash

# 1. Project folder me jao (Folder ka naam ekdum theek kar diya hai)
cd /volume1/docker/Projects/Nrega-Bookmarks/

# --- FIX START ---
# Git permission error fix
git config --global --add safe.directory /volume1/docker/Projects/Nrega-Bookmarks
# --- FIX END ---

# 2. GitHub se naya code Forcefully khicho (Local changes ignore karke)
echo "Pulling latest code from GitHub..."
git fetch origin
git reset --hard origin/main

# 3. Docker container ko naye code ke sath rebuild karo
echo "Rebuilding Docker container..."
sudo docker-compose up -d --build

echo "Update Complete! 🚀"