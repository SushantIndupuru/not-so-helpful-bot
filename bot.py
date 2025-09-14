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

talkingChannels=[int(i) for i in (os.getenv("CHANNEL_ID").replace("[","").replace("]","").split(","))]
print(talkingChannels)
global ttsVar
ttsVar=False
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
    #channel = bot.get_channel(1279074416147300414)
    #await channel.send("@everyone I have returned... >:)")
    
@bot.listen("on_message")
async def on_message(message: Message):
    name = message.author.name if message.author.global_name == None else message.author.global_name
    messages=[]
    if message.author == bot.user:
        return
    logging.info(f"{name} sent a message: {message.content}")

    if message.channel.id not in talkingChannels:
        logging.info("wrong channel")
        return
    async for historyMessage in message.channel.history(limit=5):
        role = "assistant" if historyMessage.author == bot.user else "user"
        if role == "assistant":
            messages.append({"role": role, "content": historyMessage.content})
        else:
            tmpname = historyMessage.author.display_name
            messages.append({"role": role, "content": tmpname+": "+historyMessage.content})
    messages=list(reversed(messages))
    for i in messages:
        print(i)
    
    
    
    await message.channel.trigger_typing()

    messageGen = aiInterface.getResponseJSON(messages)
    if messageGen.find("P.H.A.T.P.H.U.C.K.: ")!=-1:
        messageGen=messageGen.replace("P.H.A.T.P.H.U.C.K.: ", '')
    #messageGen=aiInterface.getResponse(str(name)+": "+message.content)
    if len(messageGen)>2000:
        messageGen = messageGen[0,1999]
    
    #await message.reply(messageGen,tts=ttsVar)
    #await message.reply(aiInterface.getResponse(str(name)+": "+message.content),tts=ttsVar)
    await message.reply(messageGen,tts=ttsVar)




    """if message.content == "hello" and message.author.id != bot.user.id:
        try:
          await message.channel.send(f"what's down")
        except nextcord.Forbidden:
          logging.info(f"Bot does not have permissions to send messages {message.guild.name}#{message.channel.name}")"""

@bot.slash_command(name="hello")
async def hello(interaction: Interaction):
    logging.info(f'{interaction.user.global_name} used /hello')

    await interaction.response.send_message(f"Hello {interaction.user.global_name}")

@bot.slash_command()
async def ttstoggle(interaction: Interaction):
    logging.info(f'{interaction.user.global_name} used /ttstoggle')
    global ttsVar
    ttsVar = not ttsVar
    await interaction.response.send_message("tts has been toggled to "+str(ttsVar))

@bot.slash_command()
async def printtts(interaction: Interaction):
    logging.info(f'{interaction.user.global_name} used /printtts')
    
    await interaction.response.send_message("tts is currently set to "+str(ttsVar))

if not os.getenv("TOKEN"):
    print("Please set the environment variable TOKEN.")
    sys.exit(1)

bot.run(os.getenv("TOKEN"))