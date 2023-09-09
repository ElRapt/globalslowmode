from discord import app_commands
from discord.ext.commands import has_permissions

def init_bot_commands(client, tree):

    @tree.command(name = "slowmode", description = "Launches slow mode") 
    @has_permissions(administrator = True)
    async def first_command(interaction, seconds:int, message:str):
        settings = client.server_settings.get_server_settings(str(interaction.guild.id))
        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await interaction.response.send_message("Enter a valid time", ephemeral=True)
            return
        await interaction.response.send_message("Slow mode activated", ephemeral=True)
        settings['activeSlow'] = True

    @tree.command(name = "revoke", description = "Ends true slowmode") 
    @has_permissions(administrator = True)
    async def first_command(interaction):
        settings = client.server_settings.get_server_settings(str(interaction.guild.id))

        settings['activeSlow'] = False
        await interaction.response.send_message("Slowmode revoked", ephemeral=True)

    @tree.command(name = "embedslow", description = "Launches slow mode for embeds")
    @has_permissions(administrator = True)
    async def first_command(interaction, seconds:int, message:str):
        settings = client.server_settings.get_server_settings(str(interaction.guild.id))

        try:
            settings['slowTime'] = int(seconds)
            settings['slowMessage'] = message
        except ValueError:
            await interaction.response.send_message("Enter a valid time", ephemeral=True)
            return
        await interaction.response.send_message("Embed slow activated", ephemeral=True)
        settings['embedSlow'] = True

    @tree.command(name = "embedrevoke", description = "Ends true slowmode for embeds")
    @has_permissions(administrator = True)
    async def first_command(interaction):
        settings = client.server_settings.get_server_settings(str(interaction.guild.id))

        settings['embedSlow'] = False
        await interaction.response.send_message("Embed slowmode revoked", ephemeral=True)