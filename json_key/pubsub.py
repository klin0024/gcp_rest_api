from google.oauth2 import service_account
import google.auth.transport.requests
import base64
import requests
import json

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = 'key.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
token = credentials.token

#print(token)

topic = "demo"
project = "gcp-expert-sandbox-allen"
url = 'https://pubsub.googleapis.com/v1/projects/' + project + '/topics/' + topic + ':publish'
message = 'hello2'
data = { "messages": {"data": base64.b64encode(message.encode("UTF-8")).decode("UTF-8")}}

resp = requests.post(
    url,
    data=json.dumps(data),
    headers={"Content-Type": "application/json",
             "Authorization": "Bearer " + token  })

print(resp.json())