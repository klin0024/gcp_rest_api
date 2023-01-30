import time
import jwt
import requests
import json
import base64

SERVICE_ACCOUNT_FILE = 'key.json'
key = json.loads(open(SERVICE_ACCOUNT_FILE, 'rb').read())


iss = key["client_email"]
sub = key["client_email"]
aud = 'https://pubsub.googleapis.com/'
iat = time.time()
exp = iat + 3600
PRIVATE_KEY_ID_FROM_JSON = key["private_key_id"]
PRIVATE_KEY_FROM_JSON = key["private_key"]

payload = {'iss': iss,
           'sub': sub,
           'aud': aud,
           'iat': iat,
           'exp': exp}
additional_headers = {'kid': PRIVATE_KEY_ID_FROM_JSON}
signed_jwt = jwt.encode(payload, PRIVATE_KEY_FROM_JSON, headers=additional_headers,algorithm='RS256')

#print(signed_jwt)

topic = "demo"
project = "gcp-expert-sandbox-allen"
url = 'https://pubsub.googleapis.com/v1/projects/' + project + '/topics/' + topic + ':publish'

message = 'hello world'
data = { "messages": {"data": base64.b64encode(message.encode("UTF-8")).decode("UTF-8")}}

resp = requests.post(
    url,
    data=json.dumps(data),
    headers={"Content-Type": "application/json",
             "Authorization": "Bearer " + signed_jwt  })

print(resp.json())