


GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 RTel Lazy Installer${NC}"


install_pkg() {
    if ! command -v $1 &> /dev/null; then
        echo "Installing $1..."
        pkg install $1 -y
    else
        echo "$1 is already installed."
    fi
}

install_pkg git
install_pkg python

echo -e "\n${BLUE}Enter your GitHub Username:${NC}"
read -p "Username: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "Username cannot be empty!"
    exit 1
fi

REPO_URL="https://github.com/$GITHUB_USER/RTel-github.git"

if [ -d "RTel-github" ]; then
    echo "Project folder exists. Skipping download..."
    cd RTel-github
else
    echo "Cloning repository..."

    if ! git clone $REPO_URL; then
        echo "Git clone failed. Trying wget fallback..."
        mkdir -p RTel-github
        wget -qO- https://github.com/$GITHUB_USER/RTel-github/archive/refs/heads/main.tar.gz | tar -xz -C RTel-github --strip-components=1
        cd RTel-github
    else
        cd RTel-github
    fi
fi

echo "Configuring..."
sed -i "s|arshiacomplus|$GITHUB_USER|g" frontend/config.js


ALIAS_CMD="alias rtel='cd ~/RTel-github && python -m http.server 8080 -d frontend'"
for rc in ~/.bashrc ~/.zshrc; do
    if [ -f "$rc" ] && ! grep -q "alias rtel=" "$rc"; then
        echo "$ALIAS_CMD" >> "$rc"
    fi
done

echo -e "\n${GREEN}✅ Installation Complete!${NC}"
echo -e "💡 Type ${GREEN}rtel${NC} to start."
python -m http.server 8080 -d frontend