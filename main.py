"""
PumpKraftBot by Zax71
Github: https://github.com/zax71/PunpKraftBot
"""

import discord, termcolor, yaml
from cogs.roleMenu import RoleButtonsView

def loadConfig():
    configFile = ""

    with open('config.yml', "r") as f:
            configFile = yaml.load(f, Loader=yaml.FullLoader)
    
    return configFile


config = loadConfig()

# Create intents object

intents = discord.Intents.default()
intents.guilds = True

# Create bot object

bot = discord.Bot(intents=intents)



""" Events """
@bot.event
async def on_ready():
    termcolor.cprint(f"Bot started. Successfully logged in as {bot.user}", "green", attrs=["bold"])
    bot.add_view(RoleButtonsView())

@bot.slash_command(guild_ids=[config["guild_ID"]], description="Pong... Hopefully")
async def ping(ctx):
    await ctx.respond("Pong")



# Load cogs
bot.load_extension("cogs.roleMenu")

bot.run(config["bot_token"])