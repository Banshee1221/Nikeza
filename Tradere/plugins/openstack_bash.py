import subprocess

magnum_port = 9511

class Plugin:
    template = ""
    token = ""

    def __init__(self, user, passwd):
        print("!!!!!" + user + " " + passwd)
        token_req = 'curl -si -d \'{"auth":{"identity":{"methods":["password"], "password":{"user":{"domain":{"id":"default"}, "name":"' + str(
            user) + '","password":"' + str(
            passwd) + '"}}}}}\' -H "Content-type: application/json" http://localhost:35357/v3/auth/tokens | awk \'/X-Subject-Token/ {print $2}\''

        # print(token_req)
        process = subprocess.run(token_req, shell=True, stdout=subprocess.PIPE)
        self.token = process.stdout.strip()

    def queue_list(self):
        command = 'curl -si -H"X-Auth-Token:' + str(
            self.token) + '" -H "Content-type: application/json" http://localhost:35357/v3/users'
        print(command)
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        print(process.stdout)
