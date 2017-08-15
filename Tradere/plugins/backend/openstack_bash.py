import json
import subprocess

fqdn = "controller.cluster"
magnum_port = "9511"
nova_port = "8774"
imageRef = "8a21c523-e682-4288-ab31-4c8102cae1d6"
flavorRef = "add2b58d-4a2b-406d-b51e-41173234738e"
keyPair = "eugene"
networkRef = "2fc73fb3-9815-4338-aac8-17b17165f91b"
networkName = "campus"
secGroup = "default"


class Plugin:
    template = ""
    token = ""
    id = ""
    result_json = ""

    def __init__(self, user, passwd):
        # print("openstack_plugin______")
        token_req = 'curl -s -d \'{"auth": {"tenantName": "' + str(
            user) + '", "passwordCredentials": {"username": "' + str(user) + '", "password": "' + str(
            passwd) + '"}}}\' -H "Content-type: application/json" http://localhost:35357/v2.0/tokens'

        process = subprocess.run(token_req, shell=True, stdout=subprocess.PIPE)
        self.result_json = json.loads(process.stdout.strip().decode('utf-8'))
        try:
            self.token = str(self.result_json['access']['token']['id'])
            # print(self.token)
        except TypeError:
            print("error, token not found")
            raise Exception
        self.id = str(self.result_json['access']['token']['tenant']['id'])

    # def queue_list(self):
    #    command = 'curl -si -H"X-Auth-Token:{0}" -H "Content-type: application/json" http://{1}:{2}/v1/clusters'.format(
    #        str(self.token), str(fqdn), str(magnum_port))
    #    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    #    return get_json(process.stdout.decode('utf-8'), 11)

    def queue_list(self):
        command = 'curl -si -H"X-Auth-Token:{0}" -H "Content-type: application/json" http://{1}:{2}/v2.1/{3}/servers/detail'.format(
            self.token, fqdn, nova_port, self.id)
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        return get_json(process.stdout.decode('utf-8'), 10)

    # def stop_job(self, clusterId):
    #    stop_req = 'curl -s -g -i -X DELETE http://' + fqdn + ':' + magnum_port + '/v1/clusters/' + str(
    #        clusterId) + ' -H"OpenStack-API-Version: container-infra latest" -H"X-Auth-Token: ' + self.token + '" -H "Content-Type: application/octet-stream" -H "User-Agent: None"'
    #    process = subprocess.run(stop_req, shell=True, stdout=subprocess.PIPE)

    def start_job(self, jobName, userData):
        # Create volume
        # Image
        # Start instance with vol and img

        start_req = """curl -X POST -H "X-Auth-Token:{0}" -H "Content-Type: application/json" -d  '
{{
 "server": {{
   "name": "{1}",
   "imageRef": "{2}",
   "flavorRef": "{3}",
   "key_name" : "{4}",
   "networks": [{{"network": "{5}", "uuid": "{5}"}}],
   "security_groups": [{{"name": "{6}"}}],
   "user_data": "{7}"
 }}
}}' http://{8}:{9}/v2/servers""".format(self.token, jobName, imageRef, flavorRef, keyPair, networkRef, secGroup, userData, fqdn, nova_port)

#        start_req = 'curl -X POST -H "X-Auth-Token:'+self.token+'" -H "Content-Type: application/json" -d "'+"{{'server': {{'name': '{0}', 'imageRef': '{1}', 'flavorRef': '{2}', 'key_name': '{3}', 'networks': [{{'network': '{4}', 'uuid': '{4}'}}], 'security_groups': [{{'name': '{5}'}}], 'user_data': '{6}'}}}}".format(jobName, imageRef, flavorRef, keyPair, networkRef, secGroup, userData)+'" http://{0}:{1}/v2/servers'.format(
#            fqdn, nova_port)
        print("\n\n\n{0}".format(start_req))
        process = subprocess.run(start_req, shell=True, stdout=subprocess.PIPE)  # Non-cred functions
        return json.loads(process.stdout.decode('utf-8'))['server']['id']

    def stop_job(self, serverId):
        stop_req = 'curl -H "X-Auth-Token:{0}" -X DELETE -H "Content-type: application/json" http://{1}:{2}/v2.1/servers/{3}'.format(
            self.token, fqdn, nova_port, serverId)
        process = subprocess.run(stop_req, shell=True, stdout=subprocess.PIPE)
        print(process.stdout)# Non-cred functions

    def get_instance_ip(self, instanceId):
        stop_req = 'curl -H "X-Auth-Token:{0}" -X GET -H "Content-type: application/json" http://{1}:{2}/v2.1/servers/{3}'.format(
            self.token, fqdn, nova_port, instanceId)
        process = subprocess.run(stop_req, shell=True, stdout=subprocess.PIPE)  # Non-cred functions
        return json.loads(process.stdout.decode('utf-8'))['server']['addresses'][str(networkName)][0]['addr']


def get_json(response, lineNum, multiline=True):
    if multiline:
        return json.loads(response.splitlines()[lineNum])
    return json.loads(response.split()[lineNum])
