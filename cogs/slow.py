import discord
from discord.ext import commands
from database.settings import get_channel_settings, set_channel_settings, ensure_channel_settings

class Slow(commands.Cog):

    @discord.slash_command(description="Setup the slowmode in this channel")
    async def slowmode(self, ctx, seconds: int, message: str):
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)

        # Ensure the channel settings exist
        ensure_channel_settings(channel_id, guild_id)

        # Fetch the channel settings
        settings = get_channel_settings(channel_id)

        # Check if settings are correctly fetched
        if settings is None:
            await ctx.respond("Failed to retrieve channel settings.", ephemeral=True)
            return

        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await ctx.respond("Enter a valid time", ephemeral=True)
            return

        await ctx.respond("Slow mode activated", ephemeral=True)
        settings['activeSlow'] = True
        set_channel_settings(channel_id, settings)

    @discord.slash_command(description="End the slowmode in this channel")
    async def revoke(self, ctx):
        settings = get_channel_settings(str(ctx.guild.id))
        ensure_channel_settings(str(ctx.channel.id), str(ctx.guild.id))
        settings['activeSlow'] = False
        set_channel_settings(str(ctx.guild.id), settings)
        await ctx.respond("Slowmode revoked", ephemeral=True)


def setup(bot):
    bot.add_cog(Slow(bot))