import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from introduction_flow import start_introduction
from onboarding_button import setup_onboarding_message  # <-- import here

intents = discord.Intents.default()
intents.members = True  # required for detecting joins
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1428528530261545061  # replace with your #welcome channel ID
INTRODUCTIONS_CHANNEL_ID = 1428279420254425179  # replace with your #introductions channel ID
#ROLE_ID = 111111111111111111  # optional: replace with your 'New Member' role ID

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    intro_channel = bot.get_channel(INTRODUCTIONS_CHANNEL_ID)

    dm_channel = await member.create_dm()
    print(f"Welcome: ✅ DM Channel ID for {member.name}: {dm_channel.id}")

    # Create button
    view = discord.ui.View()
    button = discord.ui.Button(label="👋 Introduce Yourself", style=discord.ButtonStyle.primary, url=f"https://discord.com/channels/@me/{dm_channel.id}")
    view.add_item(button)

    # Send public welcome
    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}, {member.name}! 🎉",
        description=(
            f"You're now part of **DataVerse** — a creative space where data meets imagination, "
            f"and learners become builders.\n\n"
            f"👉 Click below to **introduce yourself** and start connecting with other data enthusiasts!"
        ),
        color=0x5865F2
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    await channel.send(embed=embed, view=view)

    # Send private DM
    #try:
    #    await member.send(
    #        f"👋 Hey {member.name}, welcome to **{member.guild.name}!**\n\n"
    #        f"Make sure to check out {intro_channel.mention} and introduce yourself!\n"
    #    )
    #except:
    #    print("❌ Could not send DM")


    # Trigger the introduction sequence
    await setup_onboarding_message(bot)  # <-- Post the onboarding message in #general
    await start_introduction(bot, member, intro_channel)


bot.run(os.getenv("TOKEN"))
