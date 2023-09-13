# Global Slow Mode 

This bot helps enforce a global slow mode in a discord server. It offers both standard and embed slow modes, which can be managed separately.

All servers have their own settings, which are stored in the database. This ensures resilience in case the bot goes down.

## Table of Contents
- [Features](#features)
- [Commands](#commands)
- [License](#license)

## Features

- **Global Slow Mode**: You can enforce a slow mode where every member has to wait for a specified amount of time between their messages.
- **Global Embed Slow Mode**: You can enforce a slow mode where every member has to wait for a specified amount of time between their messages containing embeds or attachments.
- **Custom Message**: You can set a custom message that will be sent to members who attempt to send messages too frequently.
- **Admin Control**: All bot commands can only be executed by administrators.

## Commands

All commands are slash commands. Here are the commands you can use:

- `/slowmode {seconds} {message}`: Launches the global slow mode. The `seconds` parameter sets the waiting time between messages, and the `message` parameter sets the message that will be sent to users who attempt to send messages too frequently.

- `/revoke`: Ends the global slow mode.

- `/embedslow {seconds} {message}`: Launches the global slow mode for messages with embeds or attachments. The `seconds` parameter sets the waiting time between messages, and the `message` parameter sets the message that will be sent to users who attempt to send messages too frequently.

- `/embedrevoke`: Ends the global slow mode for messages with embeds or attachments.



## License

This project is licensed under the MIT License.
