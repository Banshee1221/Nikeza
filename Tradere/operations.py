import importlib
import gzip
from time import sleep
import base64
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

    def create_job(self, name, eyedee, stuffToAdd):
        ci_cript = open('operations/cloud-init.yml')
        data = ci_cript.read() + "{0}".format(stuffToAdd)
        print(data)
        sendData = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        ci_cript.close()
        job_id = self.plug.start_job("{0}_{1}".format(name, eyedee), sendData)
        #print(job_id)
        #sleep(5)
        #print(self.plug.get_instance_ip(job_id))

    def create_script(self, uid, fileName, args):

        copyfile("operations/" + str(get_settings()['operations']['ops_postscript']), "runtime/"+str(uid)+".sh")
        overall = "bootcmd:\n" \
                  "  - mkdir -p {0}\n" \
                  "  - mkdir -p {1}\n" \
                  "  - dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo\n".format(args['in_mnt'], args['out_mnt'])

        userScript = open('runtime/{0}'.format(fileName))
        userScriptData = userScript.read()
        print(userScriptData)
        userScript.close()
        b64userScriptData = base64.b64encode(userScriptData.encode('utf-8')).decode('utf-8')
        overall += "write_files:\n" \
                   "  - encoding: b64\n" \
                   "    content: {0}\n" \
                   "    path: {1}/{2}\n" \
                   "    owner: fedora:fedora\n" \
                   "runcmd:\n" \
                   "  - dnf -y install docker-ce" \
                   "  - yes | pip install cwlref-runner\n" \
                   "  - groupadd docker\n" \
                   "  - gpasswd -a fedora docker\n" \
                   "  - systemctl enable docker\n" \
                   "  - systemctl start docker\n" \
                   "  - chown -R fedora:fedora {3}\n" \
                   "  - chown -R fedora:fedora {4}\n".format(b64userScriptData, args['in_mnt'], fileName, args['out_mnt'], args['in_mnt'])

        for item in args['in_dat']:
            download_command = "cd {0} && {{ curl -O {1} ; cd -; }}\n".format(args['in_mnt'],
                                                                            self.stor.getURL(item['container'],
                                                                                             item['fileName']))
            overall += "  - {0}".format(download_command)
        overall += "  - cd {0}\n".format(args['out_mnt'])
        overall += "  - {0}\n".format(args['args'])
        overall += "  - cd {0} && cwl-runner {1}\n".format(args['in_mnt'], args['args'])

        self.create_job(fileName, uid, overall)



if __name__ == "__main__":
    ops = Ops("one", "two")
    # print(ops.get_queue())
