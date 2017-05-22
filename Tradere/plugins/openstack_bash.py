import os
import subprocess


class Plugin:
    template = ""

    def __init__(self, user, passwd):
        os.environ['OS_USERNAME'] = user
        os.environ['OS_PASSWORD'] = passwd
        os.environ['OS_PROJECT_NAME'] = user
        os.environ['OS_USER_DOMAIN_NAME'] = "Default"
        os.environ['OS_PROJECT_DOMAIN_NAME'] = "Default"
        os.environ['OS_AUTH_URL'] = "http://controller.cluster:35357/v3"
        os.environ['OS_IDENTITY_API_VERSION'] = "3"
        os.environ['OS_IMAGE_API_VERSION'] = "2"

    def queue_list(self):
        p = subprocess.check_output(['magnum', "cluster-list"])
        return p
