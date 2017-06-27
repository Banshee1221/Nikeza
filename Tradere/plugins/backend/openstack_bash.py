import json
import subprocess

fqdn = "controller.cluster"
magnum_port = "9511"


class Plugin:
    template = ""
    token = ""
    id = ""
    result_json = ""

    def __init__(self, user, passwd):
        print("openstack_plugin______")
        token_req = 'curl -s -d \'{"auth": {"tenantName": "' + str(
            user) + '", "passwordCredentials": {"username": "' + str(user) + '", "password": "' + str(
            passwd) + '"}}}\' -H "Content-type: application/json" http://localhost:35357/v2.0/tokens'

        process = subprocess.run(token_req, shell=True, stdout=subprocess.PIPE)
        self.result_json = json.loads(process.stdout.strip().decode('utf-8'))
        try:
            self.token = str(self.result_json['access']['token']['id'])
            print(self.token)
        except TypeError:
            print("error, token not found")
            raise Exception
        self.id = str(self.result_json['access']['token']['tenant']['id'])

    def queue_list(self):
        command = 'curl -si -H"X-Auth-Token:{0}" -H "Content-type: application/json" http://{1}:{2}/v1/clusters'.format(
            str(self.token), str(fqdn), str(magnum_port))
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        return get_json(process.stdout.decode('utf-8'), 11)

    def stop_job(self, clusterId):
        stop_req = 'curl -g -i -X DELETE http://' + fqdn + ':' + magnum_port + '/v1/clusters/' + str(
            clusterId) + ' -H"OpenStack-API-Version: container-infra latest" -H"X-Auth-Token: ' + self.token + '" -H "Content-Type: application/octet-stream" -H "User-Agent: None"'
        process = subprocess.run(stop_req, shell=True, stdout=subprocess.PIPE)



# Non-cred functions

def get_json(response, lineNum, multiline=True):
    if multiline:
        return json.loads(response.splitlines()[lineNum])
    return json.loads(response.split()[lineNum])
