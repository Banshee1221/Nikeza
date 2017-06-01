import json
import subprocess

fqdn = "controller.cluster"
magnum_port = 9511

class Plugin:
    template = ""
    token = ""

    def __init__(self, user, passwd):
        token_req = 'curl -si -d \'{"auth":{"identity":{"methods":["password"], "password":{"user":{"domain":{"id":"default"}, "name":"' + str(
            user) + '","password":"' + str(
            passwd) + '"}}}}}\' -H "Content-type: application/json" http://localhost:35357/v3/auth/tokens'

        # print(token_req)
        process = subprocess.run(token_req, shell=True, stdout=subprocess.PIPE)
        result_str = process.stdout.strip().decode('utf-8')
        if "X-Subject-Token" not in result_str:
            print("error, token not found")
            raise Exception
        result_arr = result_str.splitlines()
        indices = [i for i, s in enumerate(result_arr) if 'X-Subject-Token' in s]
        token_str = result_arr[indices[0]].split(":")[1].strip()
        self.token = str(token_str)

    def magnum_queue_list(self):
        command = 'curl -si -H"X-Auth-Token:{0}" -H "Content-type: application/json" http://{1}:{2}/v1/clusters'.format(
            str(self.token), str(fqdn), str(magnum_port))
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        return get_json(process.stdout.decode('utf-8'), 11)

    def stop_cluster(self, clusterId):
        pass

    def swift(self):
        #curl -s -d '{"auth": {"tenantName": "user", "passwordCredentials": {"username": "user", "password": "pass"}}}' -H 'Content-type: application/json' http://localhost:35357/v2.0/tokens | python -m json.tool
        pass


# Non-cred functions

def get_json(response, lineNum, multiline=True):
    if multiline:
        return json.loads(response.splitlines()[lineNum])
    return json.loads(response.split()[lineNum])
