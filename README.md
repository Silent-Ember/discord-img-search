# 🔍 Discord Image Search Bot

A powerful Discord bot for **reverse image searching** using [Google Lens](https://lens.google/) & [SerpApi](https://serpapi.com/).  
Helps moderators **verify images, catch fakes, and prevent catfishing** directly inside Discord.

---

## ✨ Features
- 🔍 **Reverse Image Search** – Quickly find visually similar images across the web.
- 🏆 **Top Match Highlight** – The best match is clearly featured.
- 🖼 **Full-Size Preview** – The uploaded image is shown in the embed.
- 📦 **Catbox Upload Integration** – Simple, free, bot-friendly hosting.
- 🔒 **Role-Based Permissions** – Auto-creates a role (`Image Search Perms`) for authorized users.
- ⚡ **Modern Design** – Beautiful embeds with clean, clickable results.

---

## 💬 Support
For any questions:  
- DM **[ImpactGamin](https://discord.com/users/1139024274456334401)**  
- Join the **[Discord Server](https://discord.gg/3dfSvJXRhk)**  

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/your-username/discord-img-search.git
cd discord-img-search
```
### 2. Create a Virtual Environment
```
python -m venv venv
```
Windows
```
.\venv\Scripts\activate
```
Mac/Linux
```
source venv/bin/activate
```
### 3. Upgrade pip
If you don’t have Python, install it [here](https://www.python.org/downloads) 
```
python -m pip install --upgrade pip
```

### 4. Install Dependencies
```
pip install -r requirements.txt
```
If you don’t have requirements.txt, install manually:
```
pip install discord.py google-search-results aiohttp
```
### 5. Configure Your Bot
1. Get a Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications).
2. Get a SerpApi API Key from [SerpApi](https://serpapi.com).
3. Open `image_search_bot.py` and replace:
```
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
SERPAPI_KEY = "YOUR_SERPAPI_KEY"
```
### 6. Run the Bot
```
python image_search_bot.py
```
