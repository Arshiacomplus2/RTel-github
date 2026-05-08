#!/bin/bash
pkg update && pkg upgrade -y
pkg install git python -y
if[ -d "RTel-github" ]; then 
    cd RTel-github && git pull
else 
    git clone https://github.com/arshiacomplus/RTel-github.git && cd RTel-github
fi
read -p "Enter your GitHub username: " GITHUB_USER
sed -i "s|arshiacomplus|$GITHUB_USER|g" frontend/config.js
echo "Installation complete."
echo "Run: python3 -m http.server 8080 -d frontend"
