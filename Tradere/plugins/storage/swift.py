#
#   This module requires the OpenStack backend be used, as it relies on the OpenStack user/pass
#
import json
import ast
import subprocess


class Storage:

    url = "controller.cluster"
    port = "8080"
    token = None
    result_json = None
    id = None

    def __init__(self, user, passwd, tenant):
        #print("openstack_plugin______")
        token_req = 'curl -s -s -d \'{"auth": {"tenantName": "' + str(
            tanant) + '", "passwordCredentials": {"username": "' + str(user) + '", "password": "' + str(
            passwd) + '"}}}\' -H "Content-type: application/json" http://localhost:35357/v2.0/tokens'

        process = subprocess.run(token_req, shell=True, stdout=subprocess.PIPE)
        self.result_json = json.loads(process.stdout.strip().decode('utf-8'))
        try:
            self.token = str(self.result_json['access']['token']['id'])
            #print(self.token)
        except TypeError:
            print("error, token not found")
            raise Exception
        self.id = str(self.result_json['access']['token']['tenant']['id'])
        #print(self.id)

    def overview(self):
        #return ''
        process_str = 'curl -s -i http://'+ self.url+ ':'+ self.port +'/v1/AUTH_' + str(
            self.id)+'?format=json -X GET -H "X-Auth-Token: '+str(self.token)+'"'
        process = subprocess.run(process_str, shell=True, stdout=subprocess.PIPE)
        result = str(process.stdout.strip().decode('utf-8').split("\n")[-1])
        #print(result)
        #return swift_overview_formatter(result)
        retArr = []
        for items in ast.literal_eval(result):
            retArr.append({"id": items['name'], "text": items['name'], "children": True, "type": "root"})
        return retArr

    def traverse(self, container):
        process_str = 'curl -s -i http://'+ self.url+ ':'+ self.port +'/v1/AUTH_' + str(
            self.id) + '/'+str(container)+'?format=json -X GET -H "X-Auth-Token: ' + str(self.token) + '"'
        process = subprocess.run(process_str, shell=True, stdout=subprocess.PIPE)
        result = str(process.stdout.strip().decode('utf-8').split("\n")[-1])
        retArr = []
        for items in ast.literal_eval(result):
            retArr.append({"id": items['name'], "text": items['name'], "children": False, "type": "child"})
        return retArr

    def getId(self):
        return self.id

    def getToken(self):
        return self.token

    def getURL(self, container, item):
        stringToSend = "http://{0}:{1}/v1/AUTH_{2}/{3}/{4}".format(self.url, self.port, self.id, container, item)
        return stringToSend

def swift_overview_formatter(json_in, type="inner"):
    newDict = {}
    parsedList = ast.literal_eval(json_in)
    #for k in parsedList:
    #   print(k['name'])
    return ""
