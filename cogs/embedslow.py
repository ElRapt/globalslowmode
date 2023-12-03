import discord
from discord.ext import commands
from database.settings import get_server_settings, update_server_settings, set_default_server_settings


class EmbedSlow(commands.Cog):

    @discord.slash_command(description="Setup the slowmode for embeds in this channel")
    async def embedslow(self, ctx, seconds: int, message: str):
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

        await ctx.respond("Embed slow activated", ephemeral=True)
        settings['embedSlow'] = True
        update_server_settings(str(ctx.guild.id), settings)

    @discord.slash_command(description="End the slowmode for embeds in this channel")
    async def embedrevoke(self, ctx):
        settings = get_server_settings(str(ctx.guild.id))
        if not settings:
            set_default_server_settings(str(ctx.guild.id))
            settings = get_server_settings(str(ctx.guild.id))

        settings['embedSlow'] = False
        update_server_settings(str(ctx.guild.id), settings)
        await ctx.response.send_message("Embed slowmode revoked", ephemeral=True)

def setup(bot):
    bot.add_cog(EmbedSlow(bot))