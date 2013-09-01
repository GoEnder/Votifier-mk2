import simplejson as json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256, SHA512
from Crypto.Signature import PKCS1_v1_5 
import base64
import redis
import time
import flask
import socket
from multiprocessing import Process
from flask import Flask, url_for, request, render_template, Response, redirect

app = Flask(__name__)

host = '127.0.0.1'
port = 8834

def connect():
  "Connects to Redis Database"
  return redis.StrictRedis(host='127.0.0.1', port=6379, db=42)

def sendToken(token, domain):
  time.sleep(3)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((domain, 55655))
  s.sendall(token)
  s.close()
  return

def checkSubmit(token, con=connect()):
  "Makes sure the TOKEN doesn't exist, Then allows it to pass"
  if con.hexists('tokens', token):
    return False
  else:
    return True

def decryptMessage(self, private, message):
  rsakey = RSA.importKey(private) 
  rsakey = PKCS1_OAEP.new(rsakey) 
  decrypted = rsakey.decrypt(base64.b64decode(message)) 
  return decrypted

def checkSignature(public, signature, secret):
  rsakey = RSA.importKey(public) 
  signer = PKCS1_v1_5.new(rsakey) 
  digest = SHA256.new() 
  digest.update(secret) 
  if signer.verify(digest, base64.b64decode(signature)):
    return True
  return False

def listSite(token, domain, detail, public):
  pass

def encryptMessage(key, message):
  rsakey = RSA.importKey(key) 
  rsakey = PKCS1_OAEP.new(rsakey) 
  encrypted = rsakey.encrypt(message) 
  return encrypted.encode('base64')

def genToken(public, domain):
  bits = 2
  domain = domain.strip('.')
  token = public.split(' ')[1][-20:]
  n = len(token)/bits
  n = len(domain)/bits
  token = [token[i:i+n] for i in range(0, len(token), n)]
  sdomain = [domain[i:i+n] for i in range(0, len(domain), n)]
  token = "%s%s%s%s" % (token[0],sdomain[1],token[1],sdomain[0])
  shahash = SHA256.new(token)
  token = shahash.hexdigest()
  return token

def genSecret(time, public, token):
  bits = 6
  secret = "%s" % time
  public = public.split(' ')[1]
  token = [token[i:i+len(token)/bits] for i in range(0, len(token), len(token)/bits)][0:bits]
  public = [public[i:i+len(public)/bits] for i in range(0, len(public), len(public)/bits)][0:bits]
  for i in range(0, bits):
    secret = secret + token[0]
    secret = secret + public[0]
  shahash = SHA512.new(secret)
  secret = shahash.hexdigest()
  return secret

@app.route("/api/list.json", methods=['GET', 'POST'])
def listRequest():
  rinput = request
  if len(rinput.data) == 0:
    return json.dumps(dict(result=False, err="No Payload - No data was recieved"))
  else:
    message = rinput.get_json()
    public = message['list_public']
    domain = message['list_domain']
    detail = message['list_detail']
    token = genToken(public, domain)
    secret = genSecret(time.time(), public, token)
    reply = encryptMessage(public, secret)
    reply = dict(token=token, message=reply, url='http://127.0.0.1:8834/api/verify.json')
    public = "ssh-rsa %s %s" % (public.split(' ')[1],domain)
    result = checkSubmit(token)
    if (result):
      try:
        thread = Process(target=sendToken, args=(json.dumps(reply), domain))
        thread.start()
      except Exception, e:
        print e
      connect().hset('tokens', token, json.dumps(dict(token=token, domain=domain, secret=secret, detail=detail, public=public)))
      return json.dumps(dict(result=True))
    else:
      return json.dumps(dict(result=False, err="Key already listed - This key is already in the Central Key Repository"))


@app.route("/api/verify.json", methods=['POST'])
def verifySecret():
  rinput = request
  if len(rinput.data) == 0:
    return json.dumps(dict(result=False))
  else:
    message = rinput.get_json()
    compare = json.loads(connect().hget('tokens', message['token']))
    result = checkSignature(compare['public'], message['message'], compare['secret'])
    if (result):
      return json.dumps(dict(result='Confirmed'))
    else:
      return json.dumps(dict(result='Rejected',err='Invalid Signature - Private Key/Public Key Missmatch'))
  

if __name__ == "__main__":
    app.run(host=host,port=port,debug=True)