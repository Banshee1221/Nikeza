import importlib
import base64
from time import sleep
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

    def create_script(self, uid, fileName, args):

        copyfile("operations/" + str(get_settings()['operations']['ops_postscript']), "runtime/"+str(uid)+".sh")
        overall = "bootcmd:\n"

        #fl = open("runtime/"+str(uid)+".sh", "a+")
        #fl.write("\n")
        # Lines
        input_dir_mount = "mkdir -p {0}\n".format(args['in_mnt'])
        overall += "  - {0}".format(input_dir_mount)
        #fl.write(input_dir_mount)

        output_dir_mount = "mkdir -p {0}\n".format(args['out_mnt'])
        overall += "  - {0}".format(output_dir_mount)
        #fl.write(output_dir_mount)

        overall += "runcmd:\n"

        for item in args['in_dat']:
            download_command = "cd {0} && {{ curl -O {1} ; cd -; }}\n".format(args['in_mnt'],
                                                                            self.stor.getURL(item['container'],
                                                                                             item['fileName']))
            overall += "  - {0}".format(download_command)
            #fl.write(download_command)

        working_dir = "cd {0}\n".format(args['out_mnt'])
        overall += "  - {0}".format(working_dir)
        #fl.write(working_dir)

        command = "{0}\n".format(args['args'])
        overall += "  - {0}".format(command)
        #fl.write(command)

        #fl.close()

        userScript = open('runtime/{0}'.format(fileName))
        userScriptData = userScript.read()
        userScript.close()
        b64userScriptData = base64.b64encode(userScriptData.encode('utf-8')).decode('utf-8')
        overall += "write_files:\n  - path: {2}/{0}\n  - encoding: b64\n  - content: {1}\n  - owner: fedora:fedora\nruncmd:\n  - bash {2}/{0}".format(fileName, b64userScriptData, args['in_mnt'])

        self.create_job(uid, overall)

    def create_job(self, eyedee, stuffToAdd):
        ci_cript = open('operations/cloud-init.yml')
        data = ci_cript.read() + "\n{0}".format(stuffToAdd)
        print(data)
        sendData = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        ci_cript.close()
        job_id = self.plug.start_job(eyedee, sendData)
        print(job_id)
        sleep(5)
        print(self.plug.get_instance_ip(job_id))



if __name__ == "__main__":
    ops = Ops("one", "two")
    # print(ops.get_queue())
