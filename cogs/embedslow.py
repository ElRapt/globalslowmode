import discord
from discord.ext import commands
from database.settings import get_channel_settings, set_channel_settings, ensure_channel_settings

class EmbedSlow(commands.Cog):

    @commands.has_permissions(administrator = True)
    @discord.slash_command(description="Setup the slowmode for embeds in this channel")
    async def embedslow(self, ctx, seconds: int, message: str):
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        
        ensure_channel_settings(channel_id, guild_id)
        settings = get_channel_settings(channel_id)

        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await ctx.respond("Enter a valid time", ephemeral=True)
            return

        await ctx.respond("Embed slow activated", ephemeral=True)
        settings['embedSlow'] = True
        set_channel_settings(channel_id, settings)

    @commands.has_permissions(administrator = True)
    @discord.slash_command(description="End the slowmode for embeds in this channel")
    async def embedrevoke(self, ctx):
        channel_id = str(ctx.channel.id)
        ensure_channel_settings(channel_id, str(ctx.guild.id))
        settings = get_channel_settings(channel_id)

        settings['embedSlow'] = False
        set_channel_settings(channel_id, settings)
        await ctx.respond("Embed slowmode revoked", ephemeral=True)

def setup(bot):
    bot.add_cog(EmbedSlow(bot))
