import sys
import os
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)
if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)

bot = commands.Bot()

@bot.slash_command()
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello!")

if not os.getenv("TOKEN"):
    print("Please set the environment variable TOKEN.")
    sys.exit(1)
bot.run(os.getenv("TOKEN"))