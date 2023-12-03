import discord
from discord.ext import commands
from database.settings import get_server_settings, update_server_settings, set_default_server_settings

class Slow(commands.Cog):

    @discord.slash_command(description="Setup the slowmode in this channel")
    async def slowmode(self, ctx, seconds: int, message: str):
        settings = get_server_settings(str(ctx.guild.id))
        if not settings:
            set_default_server_settings(str(ctx.guild.id))
            settings = get_server_settings(str(ctx.guild.id))

        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await ctx.respond("Enter a valid time", ephemeral=True)
            return

        await ctx.respond("Slow mode activated", ephemeral=True)
        settings['activeSlow'] = True
        update_server_settings(str(ctx.guild.id), settings)

    @discord.slash_command(description="End the slowmode in this channel")
    async def revoke_command(self, ctx):
        settings = get_server_settings(str(ctx.guild.id))
        if not settings:
            set_default_server_settings(str(ctx.guild.id))
            settings = get_server_settings(str(ctx.guild.id))
        settings['activeSlow'] = False
        update_server_settings(str(ctx.guild.id), settings)
        await ctx.respond("Slowmode revoked", ephemeral=True)


def setup(bot):
    bot.add_cog(Slow(bot))