# RTel

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

RTel is a serverless, lightweight application designed to mirror Telegram channels without requiring a dedicated backend server or VPN access. It utilizes GitHub Actions for data fetching, stores message data as static JSON files in a Git repository, and serves the content directly to a local web browser.

## Requirements
To use RTel, you only need a standard **Telegram Bot Token**. 
*Note: The bot must be added as an administrator to the target channels you wish to mirror.*

## Setup Instructions

### 1. Repository Configuration (Backend)

1. **Fork** this repository to your GitHub account.
2. Navigate to your repository's **Settings > Secrets and variables > Actions**.
3. Add the following two Repository Secrets:
   *   `TG_BOT_TOKEN`: Your Telegram Bot Token obtained from [@BotFather](https://t.me/BotFather).
   *   `TARGET_CHANNELS`: A comma-separated list of target channels (e.g., `@my_channel,@news_channel`).
4. Go to the **Actions** tab, select **Fetch Telegram Data**, and click **Run workflow** to initialize the background engine. It will automatically sync every 4 hours.

### 2. Client Installation

#### Android (via Termux)

1. Install [Termux](https://f-droid.org/en/packages/com.termux/).
2. Execute the automated installation script (replace `YOUR_USERNAME` with your GitHub username):

```bash
curl -sL https://raw.githubusercontent.com/YOUR_USERNAME/RTel-github/main/install.sh | bash
```

Once installed, you can launch the local application anytime by simply typing `rtel` in Termux and navigating to `http://localhost:8080`.

#### Desktop (Linux / macOS / Windows)

1. Clone your forked repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RTel-github.git
   cd RTel-github
   ```
2. Update `frontend/config.js` with your GitHub username.
3. Start the local server:
   ```bash
   python3 -m http.server 8080 -d frontend
   ```
4. Access the web interface at `http://localhost:8080`.