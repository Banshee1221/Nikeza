#
#   This module requires the OpenStack backend be used, as it relies on the OpenStack user/pass
#
import json
import subprocess


class Storage:

    token = None
    result_json = None
    id = None

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

    def overview(self):
        #return ''
        process_str = 'curl -i http://controller.cluster:8080/v1/AUTH_99ac7a7666064b0bba777c3a43e56c22?format=json -X GET -H "X-Auth-Token: '+str(self.token)+'"'
        process = subprocess.run(process_str, shell=True, stdout=subprocess.PIPE)
        return process.stdout.strip().decode('utf-8')
