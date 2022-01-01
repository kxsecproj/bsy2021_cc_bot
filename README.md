# BSY2021 BONUS:5
## _Bots and C&C server_

The python3 bot controlled via [gist.github](https://gist.github.com/kxsecproj/dcf75fc08e5970c9e103a885d95fa8e6) by python3 C&C server.

- Unlimited amount of bots.
- One C&C server.
- Communication via gist.github.

## Features

##### Bot's actions
- Detection of currently logged in users.
- _ls_ or _ls -a_ command on target computer for any directory.
- Running a binary by the specified path.
- Copying the file specified by path to the C&C server directory.
- Finding out the _uid_ of the current user (_uid_ for the user given by the _whoami_ command).

##### Example commands
| Action                                               | Command                           |
| ---------------------------------------------------- |:---------------------------------:|
| get list of bots                                     | bots                              |
| print help table                                     | help                              |
| kill bots and C&C                                    | terminate                         |
| get logged users from bot Alice123                   | Alice123 1                        |
| _ls /Users/myuser_ on bot Alice123                   | Alice123 2 /Users/myuser          |
| _ls -a /Users/myuser_ on bot Alice123                | Alice123 21 /Users/myuser         |
| run binary _/Users/myuser/binary_ on bot Alice123    | Alice123 3 /Users/myuser/binary   |
| copy file _/Users/myuser/file.txt_ from bot Alice123 | Alice123 4 /Users/myuser/file.txt |
| get current user's _uid_ from bot Alice123           | Alice123 5                        |

For unknown reasons, it sometimes took up to 15 seconds and sometimes a minute to execute the commands during testing. Be patient when using.

## Tech

The codes works on Linux systems. The bots communicate with the C&C server by sending images. In these pictures are hidden messages that exchange information (storage of information as in BSY: bonus3). C&C is controlled via the terminal. The bots inform about their existence by entering their name in the PlayerList.txt file, where their name and fictitious rank are located (the goal is to simulate forwarding the database to an online game). Detailed technical information about the operation of the program can be found in the code comments.

#### libraries requirements

> os \
> time \
> random \
> names (0.3.0)

#### preparation before usage and start of the application

The [bot.py](https://github.com/kxsecproj/bsy2021_cc_bot/blob/main/bot.py) and [git.py](https://github.com/kxsecproj/bsy2021_cc_bot/blob/main/git.py) files should be located in a separate folder on the infected computer. On the C&C server, [cc.py](https://github.com/kxsecproj/bsy2021_cc_bot/blob/main/cc.py) and [git.py](https://github.com/kxsecproj/bsy2021_cc_bot/blob/main/git.py) are located in a separate folder.

**infected computer**
```sh
bot_dir $ ls
bot.py git.py
bot_dir $ python3 bot.py
```

**C&C server**
```sh
cc_dir $ ls
cc.py git.py
cc_dir $ python3 cc.py
```

When the server starts, a table of commands appears (it can also be called with the _help_ command). Keep in mind that commands can be entered into the C&C server terminal only when prompted with the message **"Paste command from the table:"**. Failure to do so may cause the application to crash and damage the [gist.github](https://gist.github.com/kxsecproj/dcf75fc08e5970c9e103a885d95fa8e6) repository. Always close the application by entering the terminate password in the C&C server terminal (this is the only way to kill the server and bots and delete temporary files from the repository).

## License
MIT
