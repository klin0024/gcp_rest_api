import time
import jwt
import requests
from OpenSSL import crypto
import base64

SERVICE_ACCOUNT_FILE = 'key.p12'
auth_url = 'https://oauth2.googleapis.com/token'
p12_data = open(SERVICE_ACCOUNT_FILE, 'rb').read()

p12_password = 'notasecret'
pkey = crypto.dump_privatekey(
	crypto.FILETYPE_PEM,
	crypto.load_pkcs12(p12_data, p12_password).get_privatekey())

#print(pkey) 

iss = '138974918188-compute@developer.gserviceaccount.com'
sub = iss
scope = 'https://www.googleapis.com/auth/cloud-platform'
aud = auth_url
iat = time.time()
exp = iat + 3600

payload = {'iss': iss,
           'sub': sub,
           'scope': scope,
           'aud': aud,
           'iat': iat,
           'exp': exp}
additional_headers = {
			"alg": "RS256",
			"typ": "JWT"
	}
signed_jwt = jwt.encode(payload, pkey, headers=additional_headers,algorithm='RS256')

#print(signed_jwt)

r = requests.post(
    auth_url,
    data={
		"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
		"assertion": signed_jwt
	})

token = r.json()['access_token']

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
