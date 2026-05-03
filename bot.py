import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import asyncio
from datetime import datetime, timedelta
import re

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────
TOKEN = os.environ.get("DISCORD_TOKEN")  # Mets ton token dans les variables d'env

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ─────────────────────────────────────────
#  DONNÉES LOCALES (warns)
# ─────────────────────────────────────────
WARNS_FILE = "warns.json"

def load_warns():
    if os.path.exists(WARNS_FILE):
        with open(WARNS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warns(data):
    with open(WARNS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────
#  MOTS INTERDITS (filtre automatique)
# ─────────────────────────────────────────
BANNED_WORDS = [
    "nword", "salope", "pute", "connard", "fdp",
    # Ajoute tes mots ici
]

# ─────────────────────────────────────────
#  EVENTS
# ─────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ 77 Bot connecté en tant que {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🛡️ | !help"
        )
    )
    try:
        synced = await bot.tree.sync()
        print(f"📡 {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"Erreur sync slash : {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Filtre automatique des mots interdits
    content_lower = message.content.lower()
    for word in BANNED_WORDS:
        if word in content_lower:
            await message.delete()
            warn_embed = discord.Embed(
                title="⚠️ Message supprimé",
                description=f"{message.author.mention}, ton message contenait un mot interdit.",
                color=discord.Color.orange()
            )
            warn_embed.set_footer(text="77 Bot | Modération automatique")
            await message.channel.send(embed=warn_embed, delete_after=8)
            break

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    # Cherche le canal système ou le premier canal texte
    channel = member.guild.system_channel
    if channel is None:
        channel = next((c for c in member.guild.text_channels), None)
    if channel:
        embed = discord.Embed(
            title="👋 Bienvenue !",
            description=f"Bienvenue sur **{member.guild.name}**, {member.mention} !\nTu es le membre n°**{member.guild.member_count}**.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="77 Bot | Bienvenue")
        await channel.send(embed=embed)

@bot.event
... 
