#
#   This module requires the OpenStack backend be used, as it relies on the OpenStack user/pass
#
import json
import ast
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
        print(self.id)

    def overview(self):
        #return ''
        process_str = 'curl -i http://controller.cluster:8080/v1/AUTH_' + str(
            self.id)+'?format=json -X GET -H "X-Auth-Token: '+str(self.token)+'"'
        process = subprocess.run(process_str, shell=True, stdout=subprocess.PIPE)
        result = str(process.stdout.strip().decode('utf-8').split("\n")[-1])
        print(result)
        #return swift_overview_formatter(result)
        return ast.literal_eval(result)

    def traverse(self, container):
        process_str = 'curl -i http://controller.cluster:8080/v1/AUTH_' + str(
            self.id) + '/'+str(container)+'?format=json -X GET -H "X-Auth-Token: ' + str(self.token) + '"'
        process = subprocess.run(process_str, shell=True, stdout=subprocess.PIPE)
        result = str(process.stdout.strip().decode('utf-8').split("\n")[-1])
        print(result)
        return swift_overview_formatter(result)

def swift_overview_formatter(json_in, type="inner"):
    newDict = {}
    parsedList = ast.literal_eval(json_in)
    for k in parsedList:
        print(k['name'])
    return ""