import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Display help information for bot commands")
    async def help(self, ctx):
        # Creating an embed to display help information
        embed = discord.Embed(title="Bot Commands Help", color=discord.Color.blue())

        # Adding fields to the embed for each command
        embed.add_field(name="/embedslow [seconds] [message]", value="Setup slow mode for embeds with x seconds and message removal.", inline=False)
        embed.add_field(name="/embedrevoke", value="End the slow mode for embeds.", inline=False)
        embed.add_field(name="/lowmode [seconds] [message]", value="Setup slow mode for all messages with x seconds and message removal.", inline=False)
        embed.add_field(name="/revoke", value="End the general slow mode.", inline=False)

        # Sending the embed
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))
