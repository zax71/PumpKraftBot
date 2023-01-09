"""
PumpKraftBot by Zax71
Github: https://github.com/zax71/endercube-bot
"""
import discord, termcolor, yaml

def loadConfig():
    configFile = ""

    with open('config.yml', "r") as f:
            configFile = yaml.load(f, Loader=yaml.FullLoader)
    
    return configFile

def main():
    config = loadConfig()

    # Create bot object
    bot = discord.Bot()

    @bot.event
    async def on_ready():
        termcolor.cprint(f"Bot started. Successfully logged in as {bot.user}", "green", attrs=["bold"])

    @bot.slash_command(guild_ids=[config["guild_ID"]], description="Pong... Hopefully")
    async def ping(ctx):
        await ctx.respond("Pong")

    # Load cogs
    bot.load_extension("cogs.moderation")

    bot.run(config["bot_token"])

if __name__ == "__main__":
    main()