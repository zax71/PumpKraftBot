import discord, termcolor, yaml


""" Load Config """
def loadConfig():
    configFile = ""

    with open('config.yml', "r") as f:
            configFile = yaml.load(f, Loader=yaml.FullLoader)
    
    return configFile

config = loadConfig()

""" Create buttons """

# Individual button class
class RoleButton(discord.ui.Button):
    def __init__(self, buttonNum):
        config = loadConfig()
        super().__init__(
            label = config["roles"][buttonNum]["displayName"],
            custom_id = config["roles"][buttonNum]["displayName"],
            style = discord.ButtonStyle.blurple,
            emoji = config["roles"][buttonNum]["emoji"]
        )
        self.buttonNum = buttonNum
        self.config = config
    
    async def callback(self, interaction):
        guild = interaction.guild
        user = interaction.user
        role = guild.get_role(self.config["roles"][self.buttonNum]["id"])
        roleName = self.config["roles"][self.buttonNum]["displayName"]
        
        if user.get_role(role.id) == None:
            await user.add_roles(role)
            await interaction.response.send_message(f"Added role {roleName}", ephemeral=True)
        else:
            await user.remove_roles(role)
            await interaction.response.send_message(f"Removed role {roleName}", ephemeral=True)


# Create button view
class RoleButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Loop through config
        for buttonNum in range(1, 5+1):
            # If it doesn't exist don't bug me about it
            try:
                self.add_item(RoleButton(buttonNum))
            except KeyError:
                pass


""" Command """
class RoleMenu(discord.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.config = loadConfig()
        
        termcolor.cprint("Loaded Role Menu cog", "blue")
    
    
    @discord.slash_command(guild_ids=[config["guild_ID"]], description="Sends the roles embed", name="rolemenu")
    @discord.default_permissions(manage_messages=True)
    @discord.option(
        "channel",
        discord.TextChannel,
        description="The channel to send messages in",
        required=False
    )
    async def rolemenu(self, ctx, channel: discord.TextChannel):
        if channel == None:
            channel = ctx.channel
        

        # Create embed
        embed = discord.Embed(
            color=discord.Color.from_rgb(config["embed"]["color"]["red"], config["embed"]["color"]["green"], config["embed"]["color"]["blue"]),
            title=self.config["embed"]["title"],
            description=self.config["embed"]["description"]
        )
        await ctx.respond(f"Sent Roles Embed to {channel.mention}", ephemeral=True)
        await channel.send("", view=RoleButtonsView(), embed=embed)

def setup(bot):
    bot.add_cog(RoleMenu(bot))