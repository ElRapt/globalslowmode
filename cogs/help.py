import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.has_permissions(administrator = True)
    @discord.slash_command(description="Display help information for bot commands")
    async def help(self, ctx):
        embed = discord.Embed(title="Bot Commands Help", color=discord.Color.blue())

        embed.add_field(name="/embedslow [seconds] [message]", value="Setup slow mode for embeds with x seconds and message removal.", inline=False)
        embed.add_field(name="/embedrevoke", value="End the slow mode for embeds.", inline=False)
        embed.add_field(name="/lowmode [seconds] [message]", value="Setup slow mode for all messages with x seconds and message removal.", inline=False)
        embed.add_field(name="/revoke", value="End the general slow mode.", inline=False)

        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))
