from aprsfi import API
import json



configuration = json.load(open('configuration.json'))
aprfi_api = API(configuration["aprsfi_token"])


def callAprsFi(sondenumber):
    response = aprfi_api.loc(sondenumber)
    if response.result == 'ok':
        return response.entries
        
def GetTrajectory(sondenumber):
    response = callAprsFi(sondenumber)
    for x in response:
        print(x.lat, x.lng, x.altitude)
    print(response[0].path) 
    response = callAprsFi(response[0].path)
    for x in response:
        print(x.path)
    



#Self - test
GetTrajectory("S3510480")