


GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Welcome to RTel Magic Installer!${NC}"
echo "Installing prerequisites (Git & Python)..."
pkg update -y && pkg upgrade -y
pkg install git python -y

echo -e "\n${BLUE}Please enter your GitHub Username:${NC}"
read -p "Username: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "Username cannot be empty! Exiting..."
    exit 1
fi

REPO_URL="https://github.com/$GITHUB_USER/RTel-github.git"

if[ -d "RTel-github" ]; then
    echo "Project folder already exists. Updating..."
    cd RTel-github && git pull origin main
else
    echo "Cloning your repository..."
    git clone $REPO_URL
    cd RTel-github
fi

echo "Configuring the frontend..."

sed -i "s|arshiacomplus|$GITHUB_USER|g" frontend/config.js

echo "Creating 'rtel' quick command..."

ALIAS_CMD="alias rtel='cd ~/RTel-github && python -m http.server 8080 -d frontend'"


if ! grep -q "alias rtel=" ~/.bashrc 2>/dev/null; then echo "$ALIAS_CMD" >> ~/.bashrc; fi
if [ -f ~/.zshrc ] && ! grep -q "alias rtel=" ~/.zshrc 2>/dev/null; then echo "$ALIAS_CMD" >> ~/.zshrc; fi

echo -e "\n${GREEN}✅ Installation Complete!${NC}"
echo -e "💡 Next time, just type ${GREEN}rtel${NC} in Termux to start reading messages."
echo -e "🚀 Starting the web server for the first time..."


python -m http.server 8080 -d frontend