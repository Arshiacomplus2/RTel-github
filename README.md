# RTel

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

RTel is a serverless, lightweight application designed to mirror Telegram channels without requiring a dedicated backend server or VPN access. It utilizes GitHub Actions for data fetching, stores message data as static JSON files in a Git repository, and serves the content directly to a local web browser using client-side rendering.

## Key Features

* **Network Resilience:** Retrieves raw data via GitHub's Content Delivery Network (CDN), effectively bypassing standard network restrictions.
* **Serverless Architecture:** Fully relies on GitHub Actions for scheduled background tasks, eliminating backend server hosting costs.
* **Storage Optimization:** Excludes heavy media files, implements JSON data chunking, and isolates data commits to a separate branch to prevent Git repository bloat.
* **Mobile-Optimized UI:** Includes a responsive web interface tailored for local execution on mobile devices (e.g., via Termux), featuring infinite scroll and local DOM caching.

## System Architecture

1. **Fetcher Engine (Backend):** A Python script utilizing the `Telethon` library runs periodically via GitHub Actions to fetch new text messages from specified Telegram channels.
2. **Data Storage:** Messages are parsed and saved as structured JSON chunks in a dedicated `data-branch`.
3. **Client Interface (Frontend):** A static HTML/JavaScript application running locally fetches the JSON data from GitHub's Raw URL and renders it dynamically.

## Setup Instructions

### 1. Repository Configuration (Backend)

To deploy your own instance of RTel, follow these steps:

1. **Fork** this repository to your GitHub account.
2. Obtain an `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
3. Generate a Telegram String Session (you can use a local Telethon script to generate this).
4. Navigate to your repository's **Settings > Secrets and variables > Actions**.
5. Add the following Repository Secrets:
   * `TG_API_ID`: Your Telegram API ID.
   * `TG_API_HASH`: Your Telegram API Hash.
   * `TG_SESSION`: Your generated String Session.
   * `TARGET_CHANNELS`: Comma-separated list of target channels (e.g., `@channel1,@channel2`).
6. Go to the **Actions** tab, select **Fetch Telegram Data**, and click **Run workflow** to initialize the first data fetch.

> **Security Notice:** Treat your `TG_SESSION` as a highly sensitive credential. Do not share it or commit it to the repository.

### 2. Client Installation

#### Android (via Termux)

1. Install [Termux](https://f-droid.org/en/packages/com.termux/).
2. Execute the automated installation script (replace `YOUR_USERNAME` with your GitHub username):

```bash
curl -sL https://raw.githubusercontent.com/YOUR_USERNAME/RTel-github/main/install.sh | bash
```

Once installed, you can launch the local server anytime by typing `rtel` in the Termux terminal and navigating to `http://localhost:8080` in your web browser.

#### Desktop (Linux / macOS / Windows)

1. Clone your forked repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RTel-github.git
   cd RTel-github
   ```
2. Update `frontend/config.js` with your GitHub username.
3. Start the local development server:
   ```bash
   python3 -m http.server 8080 -d frontend
   ```
4. Access the web interface at `http://localhost:8080`.
