import discord
from discord.ext import commands
from database.settings import get_channel_settings, set_channel_settings, ensure_channel_settings

class EmbedSlow(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="Setup the slowmode for embeds in this channel")
    async def embedslow(self, ctx, seconds: int, message: str):
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

        settings['embedSlowTime'] = seconds  
        settings['embedSlowMessage'] = message  
        settings['embedSlow'] = True
        set_channel_settings(channel_id, settings)

        await ctx.respond(f"Embed slow mode set for {seconds} seconds.", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @discord.slash_command(description="End the slowmode for embeds in this channel")
    async def embedrevoke(self, ctx):
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        ensure_channel_settings(channel_id, guild_id)
        settings = get_channel_settings(channel_id)

        if settings is None:
            await ctx.respond("Failed to retrieve channel settings.", ephemeral=True)
            return

        settings['embedSlow'] = False
        set_channel_settings(channel_id, settings)
        await ctx.respond("Embed slow mode revoked", ephemeral=True)

def setup(bot):
    bot.add_cog(EmbedSlow(bot))
