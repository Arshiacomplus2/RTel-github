#!/bin/bash

# Initialize git if not already
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/arshiacomplus/RTel-github.git
fi

# Create directory structure
mkdir -p .github/workflows
mkdir -p src
mkdir -p data/archive
mkdir -p frontend/assets

# Create files
touch .github/workflows/fetch.yml
touch src/fetcher.py
touch src/utils.py
touch requirements.txt

# Create JSON files
echo '[]' > data/latest.json
echo '{"archives":[]}' > data/index.json

# Create frontend files
touch frontend/index.html
touch frontend/assets/style.css
touch frontend/assets/app.js

# Create config.js
cat <<EOL > frontend/config.js
const CONFIG = {
    GITHUB_RAW_BASE_URL: "https://raw.githubusercontent.com/arshiacomplus/RTel-github/data-branch"
};
EOL

# Create installer script
cat <<'EOL' > install.sh
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
EOL

chmod +x install.sh

# Create .gitignore
cat <<EOL > .gitignore
__pycache__/
*.py[cod]
.env
*.session
*.session-journal
EOL

# Commit and push
git add .
git commit -m "Initialize project structure"
git push -u origin main