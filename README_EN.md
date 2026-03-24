# Steam Game Price Bot | Steam Game Price Assistant 🎮

<div align="center">

![Vue 3](https://img.shields.io/badge/Vue-3.5.13-4FC08D?style=flat-square&logo=vue.js)
![Vite](https://img.shields.io/badge/Vite-6.2.0-646CFF?style=flat-square&logo=vite)
![Flask](https://img.shields.io/badge/Flask-Python-000000?style=flat-square&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)

**Query Steam game prices across multiple platforms based on IsThereAnyDeal API**

[中文说明](./README.md)

</div>

---

## 📖 Project Overview

Steam Game Price Assistant is a full-stack game price query system built on the **IsThereAnyDeal** platform API. Through a concise and intuitive frontend interface, users can quickly query Steam game prices across major gaming platforms, including current lowest price, historical lowest price, and current Steam price, helping players discover the best timing for purchases. More features are under continuous development. We welcome your ideas, suggestions, and contributions!  

project update logs: [update_en.txt](./update_en.txt)

## ❓ Questions About Usage?
- If you have usage questions or encounter issues, please click 👉 [Issues Section](https://github.com/flh155/SteamGamePriceSpider/issues) to submit your questions

- If you have suggestions or feedback about the project, or want to discuss with other users, please click 👉 [Discussions Section](https://github.com/flh155/SteamGamePriceSpider/discussions) to create a post

- If you are also a developer and want to become one of the project contributors, please click 👉 [Pull Requests Section](https://github.com/flh155/SteamGamePriceSpider/pulls) to submit your feature development optimizations

### ✨ Features

- 🔍 **Real-time Price Comparison** - Query game prices across multiple platforms with one click
- 💰 **Price Tracking** - Display current discount prices and historical lowest prices to assist purchase decisions
- 🎯 **Precise Search** - Support fuzzy matching for game English names
- 🔐 **Secure Authentication** - Complete user authentication system with AES encrypted password storage
- 📱 **Responsive Design** - Modern UI interface adapted for desktop and mobile devices
- 🐳 **Containerized Deployment** - One-click deployment with Docker Compose

---

## 🚀 Main Features

### 1. Game Price Query
- Enter game name (currently only supports English names)
- Get real-time price comparison across all platforms
- Display current lowest price, historical lowest price, and current Steam price

### 2. Hot Discount Recommendations (Under Development)
- Automatically display current hot discount game lists
- Sort by popularity to discover quality discounted games
- Click to access game price details directly

### 3. More Features Under Development...

---
## 📋 Future Development Roadmap

### 1. Global Charity Bundle Tracking
- Automatically crawl charity bundle information from platforms like HumbleBundle
- Automatic price comparison to calculate charity bundle discounts

### 2. Wishlist Game Tracking
- Set up game watchlists
- Receive notifications when wishlist games go on sale or hit historical lows across platforms

---
## ⚡ Quick Start

### 1. Prerequisites
Ensure Docker and Docker Compose are installed.

### 2. Clone the Latest Main Branch
Use command `git clone https://github.com/flh155/SteamGamePriceSpider.git` to clone the latest code.

### 3. Build and Start with Docker
Navigate to the project root directory and use command `docker compose up -d --build` to build and start the project. The first build may take a few minutes.

### 4. Apply for IsThereAnyDeal API KEY
Visit [IsThereAnyDeal](https://isthereanydeal.com/apps/) official website, create an account and login, create an app, and obtain the API-KEY.

### 5. Access Frontend Page for Use
After successful build and startup, access via browser at http://localhost:3001 (local deployment).

#### First-Time User Guide
- Step 1: Initialize administrator password
- Step 2: Login to the system using the password you just set
- Step 3: Configure API Key: A configuration wizard will pop up on first launch. Enter the API Key obtained from IsThereAnyDeal (can be modified later in settings page)

---
## 🔄 Update Instructions
1. Navigate to the project root directory and execute `docker compose down` to stop frontend and backend services
2. Execute `git pull` to pull the latest code
3. Execute `docker compose up -d --build` to rebuild and start the project

---
## 🤝 Contribution Guidelines
Issues and Pull Requests are welcome!
1. Fork this repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---
## 🙏 Special Thanks
- IsThereAnyDeal: For providing powerful game price data API

---

<div align="center">If you find this project helpful, please give it a ⭐ Star! Made with ❤️ by FLH155</div>