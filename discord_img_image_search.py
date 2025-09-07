# ==== Made By Silent Ember Labs | Code Is Opensouce Use As You Please ====

import os
import sys
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from serpapi import GoogleSearch

# ==== CONFIG ====
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN" # Discord Bot Token - Find At https://discord.com/developers
SERPAPI_KEY = "YOUR_DISCORD_BOT_TOKEN" # SerpAPI Key - Find At https://serpapi.com (Account Required)
ROLE_NAME = "Image Search Perms" # Change To Whatever You Want The Role Name To Be (Does Not Auto Create - Must Be Made Manually)


# ==== BOT SETUP ====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def log(msg: str):
    print(msg)
    sys.stdout.flush()

# ==== CATBOX UPLOAD ====
async def upload_to_catbox(data: bytes, filename: str) -> str:
    """Uploads an image to Catbox.moe and returns a direct URL."""
    url = "https://catbox.moe/user/api.php"
    form = aiohttp.FormData()
    form.add_field("reqtype", "fileupload")
    form.add_field("fileToUpload", data, filename=filename, content_type="application/octet-stream")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Catbox upload failed: {resp.status}")
            text = await resp.text()
            return text.strip()

# ==== SERPAPI HELPERS ====
def serpapi_reverse(image_url: str):
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "us",
        "device": "desktop",
        "no_cache": "true"
    }
    return GoogleSearch(params).get_dict().get("image_results", [])

def serpapi_lens(image_url: str):
    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "us",
        "device": "desktop",
        "no_cache": "true"
    }
    d = GoogleSearch(params).get_dict()
    return d.get("visual_matches") or d.get("image_results") or []

# ==== EVENTS ====
@bot.event
async def setup_hook():
    log("[SETUP] Syncing global commands...")
    await bot.tree.sync()
    log("[SETUP] Commands synced globally")

@bot.event
async def on_ready():
    log(f"[READY] Logged in as {bot.user} (id={bot.user.id})")
    for guild in bot.guilds:
        if not discord.utils.get(guild.roles, name=ROLE_NAME):
            await guild.create_role(name=ROLE_NAME, reason="Role for image search permissions")
            log(f"[ROLE] Created '{ROLE_NAME}' in {guild.name}")

@bot.event
async def on_guild_join(guild: discord.Guild):
    if not discord.utils.get(guild.roles, name=ROLE_NAME):
        await guild.create_role(name=ROLE_NAME, reason="Role for image search permissions")
        log(f"[ROLE] Created '{ROLE_NAME}' in {guild.name}")

# ==== CONTEXT MENU COMMAND ====
@bot.tree.context_menu(name="Search Image")
async def search_image(inter: discord.Interaction, message: discord.Message):
    # Role check
    role = discord.utils.get(inter.guild.roles, name=ROLE_NAME)
    if not role or role not in inter.user.roles:
        return await inter.response.send_message(
            f"❌ You need the `{ROLE_NAME}` role to use this.", ephemeral=True
        )

    # Get first attachment
    attachment = next(
        (a for a in message.attachments if a.filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp"))
        ),
        None
    )
    if not attachment:
        return await inter.response.send_message("❌ No image found in that message.", ephemeral=True)

    await inter.response.defer(thinking=True)

    # Upload to Catbox
    try:
        url = await upload_to_catbox(await attachment.read(), attachment.filename)
        log(f"[UPLOAD] Uploaded to Catbox: {url}")
    except Exception as e:
        return await inter.followup.send(f"⚠️ Upload failed: {e}")

    # Search via SerpApi
    results = serpapi_reverse(url)
    if not results:
        results = serpapi_lens(url)

    # No matches
    if not results:
        embed = discord.Embed(
            title="❌ No Matches Found",
            description="I couldn't find anything for this image.",
            color=discord.Color.red()
        )
        embed.set_image(url=attachment.url)
        return await inter.followup.send(embed=embed)

    # Sort results to keep most relevant first
    # (SerpApi already gives best matches first, so we keep that order)

    # Build polished embed
    uploaded_image = attachment.url  # Discord attachment URL
    top_result = results[0]
    top_title = top_result.get("title") or "Top Match"
    top_link = top_result.get("link") or top_result.get("source") or ""
    top_thumb = top_result.get("thumbnail") or top_result.get("image", "")

    embed = discord.Embed(
        title="🔍 Reverse Image Search",
        description="Here are the closest matches I found:",
        color=discord.Color.blurple()
    )
    embed.set_image(url=uploaded_image)

    # Highlight Top Result
    if top_link:
        embed.add_field(
            name="🏆 Top Result",
            value=f"[{top_title}]({top_link})",
            inline=False
        )

    # Add other results
    for idx, item in enumerate(results[1:5], start=2):
        title = item.get("title") or f"Result {idx}"
        link = item.get("link") or item.get("source") or ""
        if link:
            embed.add_field(
                name=f"🔗 Result {idx}",
                value=f"[{title}]({link})",
                inline=False
            )

    embed.set_footer(text="Powered by SerpApi & Google Lens")
    await inter.followup.send(embed=embed)

# ==== RUN ====
bot.run(DISCORD_TOKEN)