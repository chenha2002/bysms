import  requests,pprint

payload = {

    'username':'byhy',
    "password":"88888888"
}
response = requests.session().post('http://localhost/api/mgr/signin',data=payload)
rep = response.json()
pprint.pprint(rep)
session_id = rep['session_id']

payload = {


    "action":"add"
}
headers = {
    'Content-Type': 'application/json',
    'cookie': 'sessionid='+session_id
}
response = requests.session().get('http://localhost/api/mgr/order',params=payload,headers=headers)
pprint.pprint(response.json())
