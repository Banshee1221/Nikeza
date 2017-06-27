import importlib
from parser import get_settings
from plugins.system import *

plugin = importlib.import_module("plugins.backend." + str(get_settings()['backend']['platform_file']).replace(".py", ""))
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

    def get_storage_json(self):
        return self.stor.overview()


if __name__ == "__main__":
    ops = Ops("one", "two")
    # print(ops.get_queue())
