from discord import app_commands
from discord.ext.commands import has_permissions
from database import get_server_settings, update_server_settings, set_default_server_settings

def init_bot_commands(client, tree):

    @tree.command(name="slowmode", description="Launches slow mode")
    @has_permissions(administrator=True)
    async def slowmode_command(interaction, seconds: int, message: str):
        settings = get_server_settings(str(interaction.guild.id))
        if not settings:
            set_default_server_settings(str(interaction.guild.id))
            settings = get_server_settings(str(interaction.guild.id))

        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await interaction.response.send_message("Enter a valid time", ephemeral=True)
            return

        await interaction.response.send_message("Slow mode activated", ephemeral=True)
        settings['activeSlow'] = True
        update_server_settings(str(interaction.guild.id), settings)

    @tree.command(name="revoke", description="Ends true slowmode")
    @has_permissions(administrator=True)
    async def revoke_command(interaction):
        settings = get_server_settings(str(interaction.guild.id))
        if not settings:
            set_default_server_settings(str(interaction.guild.id))
            settings = get_server_settings(str(interaction.guild.id))

        settings['activeSlow'] = False
        update_server_settings(str(interaction.guild.id), settings)
        await interaction.response.send_message("Slowmode revoked", ephemeral=True)

    @tree.command(name="embedslow", description="Launches slow mode for embeds")
    @has_permissions(administrator=True)
    async def embedslow_command(interaction, seconds: int, message: str):
        settings = get_server_settings(str(interaction.guild.id))
        if not settings:
            set_default_server_settings(str(interaction.guild.id))
            settings = get_server_settings(str(interaction.guild.id))

        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await interaction.response.send_message("Enter a valid time", ephemeral=True)
            return

        await interaction.response.send_message("Embed slow activated", ephemeral=True)
        settings['embedSlow'] = True
        update_server_settings(str(interaction.guild.id), settings)

    @tree.command(name="embedrevoke", description="Ends true slowmode for embeds")
    @has_permissions(administrator=True)
    async def embedrevoke_command(interaction):
        settings = get_server_settings(str(interaction.guild.id))
        if not settings:
            set_default_server_settings(str(interaction.guild.id))
            settings = get_server_settings(str(interaction.guild.id))

        settings['embedSlow'] = False
        update_server_settings(str(interaction.guild.id), settings)
        await interaction.response.send_message("Embed slowmode revoked", ephemeral=True)
