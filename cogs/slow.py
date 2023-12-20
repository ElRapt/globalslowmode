import discord
from discord.ext import commands
from database.settings import get_channel_settings, set_channel_settings, ensure_channel_settings


class Slow(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="Setup the slowmode in this channel")
    async def slowmode(self, ctx, seconds: int, message: str):
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)

        if seconds <= 0:
            await ctx.respond("Please enter a positive number of seconds.", ephemeral=True)
            return

        ensure_channel_settings(channel_id, guild_id)
        settings = get_channel_settings(channel_id)

        if settings is None:
            await ctx.respond("Failed to retrieve channel settings.", ephemeral=True)
            return

        settings['slowTime'] = seconds
        settings['slowMessage'] = message
        settings['activeSlow'] = True
        set_channel_settings(channel_id, settings)

        await ctx.respond(f"Slow mode set with {seconds} seconds interval.", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="End the slowmode in this channel")
    async def revoke(self, ctx):
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)

        ensure_channel_settings(channel_id, guild_id)
        settings = get_channel_settings(channel_id)

        if settings is None:
            await ctx.respond("Failed to retrieve channel settings.", ephemeral=True)
            return

        settings['activeSlow'] = False
        set_channel_settings(channel_id, settings)

        await ctx.respond("Slowmode revoked", ephemeral=True)

def setup(bot):
    bot.add_cog(Slow(bot))
