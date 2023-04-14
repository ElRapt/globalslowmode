# Discord Slowmode Bot

The Discord Slowmode Bot is a powerful tool that helps you manage the rate of messages, embeds, links, and images being sent in your Discord server. With just a few simple commands, you can easily set up global timers for messages and enforce slowmode across all channels the bot has access to. Say goodbye to spammy messages and enjoy a more organized and controlled server environment.
# Features

    Global timer for messages: Set a timer in seconds, and the bot will enforce slowmode across all channels it has access to. This means that users can only send one message every X seconds, as defined by the timer.

    Four commands:

        /slowmode(timer, message): Activates slowmode for all channels the bot has access to with a timer of timer seconds. If a user sends a message while the timer is still active, the bot will send the message message in DM and delete the original message.

        /embedslow(timer, message): Activates slowmode for embeds, links, and images only, with the same functionality as /slowmode.

        /revoke: Revokes slowmode for all channels and resets the timer.

        /embedrevoke: Revokes embed slowmode and resets the timer.

# Usage

    Create your own discord application.

    Assign the necessary permissions to the bot so that it can read and manage messages in the channels you want to enforce slowmode.

    Use the following commands to set up slowmode in your server:

    /slowmode(timer, message): Set the global timer for messages. For example, /slowmode(600, "Please wait 10 minutes between messages.") will set the timer to 10 minutes (600 seconds) and send the message "Please wait 10 minutes between messages." to users who send messages too quickly.

    /embedslow(timer, message): Set the timer for embeds, links, and images only. For example, /embedslow(300, "Slow down! You can only send embeds every 5 minutes.") will set the timer to 5 minutes (300 seconds) and send the message "Slow down! You can only send embeds every 5 minutes." to users who send embeds, links, or images too quickly.

    /revoke: Revoke slowmode for all channels and reset the timer.

    /embedrevoke: Revoke embed slowmode and reset the timer.

Note: Only users with the administrator permissions can use these commands.

Note2 : This bot shares command tree variables with all servers it is present on. As such, it is not recommanded to use on multiple servers unless you plan to set the same slowmodes.
## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the bot's GitHub repository. Contributions are always welcome and appreciated.
## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this bot as per the terms of the license.
## Credits

This Discord Slowmode Bot was developed by ElRaptou and uses discord.py. 
