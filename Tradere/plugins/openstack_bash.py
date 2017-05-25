import subprocess


class Plugin:
    template = ""
    token = ""

    def __init__(self, user, passwd):
        token_req = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "id": "default"
                            },
                            "name": user,
                            "password": passwd
                        }
                    }
                }
            }
        }

        self.token = subprocess.check_output(
            ["curl", "-si", "-d " + str(token_req) + "", "-H 'Content-type: application/json'",
             "http://localhost:35357/v3/auth/tokens | awk '/X-Subject-Token/ {print $2}'"])
        print(self.token)


    def queue_list(self):
        p = subprocess.check_output(['magnum', "cluster-list"])
        return p
