import importlib
from parser import get_settings
from shutil import copyfile

from plugins.system import *

plugin = importlib.import_module(
    "plugins.backend." + str(get_settings()['backend']['platform_file']).replace(".py", ""))
storage = importlib.import_module("plugins.storage." + str(get_settings()['system']['storage_backend']).replace(".py",
                                                                                                                ""))


class Ops:
    plug = None
    stor = None
    user = None
    passwd = None

    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.plug = plugin.Plugin(user, passwd)
        self.stor = storage.Storage(user, passwd)

    def get_queue(self):
        """
        Receives the list of running objects as dict
        :return:
        """
        return self.plug.queue_list()

    def stop_run(self, listOfIds):
        for item in listOfIds:
            if item is not None:
                self.plug.stop_job(item)

    def get_storage(self):
        return self.stor.overview()

    def get_storage_inner(self, containerName):
        return self.stor.traverse(containerName)

    def create_job(self):
        return True

    def create_script(self, uid, eyedee, args):
        userScript = open('runtime/{0}'.format(eyedee))
        print(userScript.readlines())
        userScript.close()

        copyfile("operations/" + str(get_settings()['operations']['ops_postscript']), "runtime/"+str(uid)+".sh")
        fl = open("runtime/"+str(uid)+".sh", "a+")
        fl.write("\n")
        # Lines
        input_dir_mount = "mkdir -p {0}\n".format(args['in_mnt'])
        fl.write(input_dir_mount)

        output_dir_mount = "mkdir -p {0}\n".format(args['out_mnt'])
        fl.write(output_dir_mount)

        for item in args['in_dat']:
            download_command = "cd {0} && {{ curl -O {1} ; cd -; }}\n".format(args['in_mnt'],
                                                                            self.stor.getURL(item['container'],
                                                                                             item['fileName']))
            fl.write(download_command)

        working_dir = "cd {0}\n".format(args['out_mnt'])
        fl.write(working_dir)

        command = "{0}\n".format(args['args'])
        fl.write(command)

        fl.close()

    def create_instance(self):
        self.plug.


if __name__ == "__main__":
    ops = Ops("one", "two")
    # print(ops.get_queue())
