import sys
import os
import nextcord
from nextcord import Interaction, Message
from nextcord.ext import commands, application_checks
import logging
from dotenv import load_dotenv
import aiInterface

load_dotenv()

logging.basicConfig(level=logging.INFO)
if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

# captures command errors - not listener errors!
@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error: Exception):
    logging.error(f"Error during application command execution: {error}")
    if interaction.response.is_done(): # if responded to already, leave it
        return
    if isinstance(error, nextcord.ApplicationCheckFailure):
        await interaction.response.send_message(f"You do not have permissions to use this command.")
    else:
        # Handle other unexpected errors
        await interaction.response.send_message("An error occurred during command execution.")


@bot.listen("on_ready")
async def on_ready():
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(activity=nextcord.Game(name="with your life"))

@bot.listen("on_message")
async def on_message(message: Message):
    
    if message.author == bot.user:
        return
    logging.info(f"{message.author} sent a message")
    if int(os.getenv("CHANNEL_ID"))!=message.channel.id:
        logging.info("wrong channel")
        return
    await message.channel.trigger_typing()
    await message.channel.send(aiInterface.getResponse(str(message.author)+": "+message.content))




    """if message.content == "hello" and message.author.id != bot.user.id:
        try:
          await message.channel.send(f"what's down")
        except nextcord.Forbidden:
          logging.info(f"Bot does not have permissions to send messages {message.guild.name}#{message.channel.name}")"""

@bot.slash_command()
async def hello(interaction: Interaction):
    logging.info(f'{interaction.user} used /hello')
    await interaction.response.send_message("Hello!")

if not os.getenv("TOKEN"):
    print("Please set the environment variable TOKEN.")
    sys.exit(1)

bot.run(os.getenv("TOKEN"))