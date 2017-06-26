import importlib
from parser import get_settings

plugin = importlib.import_module("plugins.user." + str(get_settings()['backend']['platform_file']).replace(".py", ""))
storage = importlib.import_module("plugins.storage." + str(get_settings()['system']['storage_backend']).replace(".py", ""))


class Ops:
    plug = None

    def __init__(self, user, passwd):
        self.plug = plugin.Plugin(user, passwd)

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


if __name__ == "__main__":
    ops = Ops("one", "two")
    # print(ops.get_queue())
