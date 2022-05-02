# BaseDiscord

A small package built on [py-cord][pycord] (since the 2.0). This package implement a base of bot with help commands, stop bot commands and other global commands.  

**Note:** This package is useful if you want use prefixed commands. To work, your bot must be authorized to read messages contents.


## Overview

 * Author: [LostPy][me]
 * Date created: 2021-06-22
 * Last update: 2022-05-02
 * Version: 2.0
 * [Documentation][doc]


## Requirements

 * [py-cord][pycord]
 * [colorama][colorama]

## Installation

To install this package, you can use
```
pip install git+https://github.com/LostPy/baseDiscord-py.git@master
```

To update the package, you can use
```
pip install -U git+https://github.com/LostPy/baseDiscord-py.git@master
```

## Main Features

|Name|Description|First Version|last version|
|----|-----------|:-----------:|:----------:|
|Manage CommandNotFound error|Ignore CommandNotFound exception|1.0|✔️|
|Manage BadArgument error|Send a error message|1.0|✔️|
|Manage MissingPermissions|Send a error message with list of permissions required|1.0|✔️|
|Manage MissingRoles|Send a error message with list of roles required|1.0|✔️|
|Manage BotMissingPermissions|Send a error message with list of permissions required|1.0|✔️|
|Manage BotMissingRoles|Send a error message with list of roles required|1.0|✔️|
|Traceback message to owner|Send a message with traceback to the owner of application if a error raised is not manage and if `BaseBot.send_errors` is `True`|1.0|✔️|
|Help cog|a [cog][cog] for help commands|1.0|✔️|
|Help slash command|A help Slash command to replace the default help command of `discord.py`|1.0|✔️|
|Owner cog|A [cog][cog] for only owner application commands|1.0|✔️|
|`stopBot`|A command of `Owner` [cog][cog] to stop the bot|1.0|✔️|
|`BaseBot.get_invitation`|Method to get a invitation link|1.0|✔️|
|Colored log|A formater for colored logs. A logger can be created with `baseDiscord.utils.new_logger` function|1.0|✔️|

> ℹ️ All message errors are send in a embed


## Changelog


[pycord]: https://docs.pycord.dev/en/master/
[colorama]: https://pypi.org/project/colorama/
[cog]: https://docs.pycord.dev/en/master/ext/commands/cogs.html
[doc]: https://lostpy.gitbook.io/basediscord-py/
[me]: https://github.com/LostPy/