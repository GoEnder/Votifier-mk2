import simplejson as json
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.Hash import SHA, SHA256
import base64
import time

#
# This is only used as an example on how Votifier-mk2 might check votes
# This is not meant to be used by you.
#

keyfile = 'id_servlist'

def checkSignature(public, signature, message):
  rsakey = RSA.importKey(public) 
  signer = PKCS1_v1_5.new(rsakey) 
  digest = SHA256.new() 
  digest.update(message) 
  if signer.verify(digest, base64.b64decode(signature)):
    return True
  return False

def splitPayload(payload):
  payload = payload.split('\xa7')
  return payload

def parseVote(payload):
  epoch = time.time()
  payload = splitPayload(payload)
  message = payload[0]
  signature = payload[1]
  public = open(keyfile+'.pub', 'r').read()
  if (checkSignature(public, signature, message)):
    message = json.loads(message)
    print "Vote recieved from %s created by %s from the IP %s" % (message['serviceName'],message['username'],message['address'])
  else: 
    print "False vote"

vote = '{"Type":"VOTE","serviceName":"","username":"KsaRedFx","address":"192.168.0.1","timestamp":"1378619747","uuid":"9d10ecca353f1f225cd95aeaa8a5f4f73d1bd263"}\xa7b5dMPcVjWX7TkS0qwzwXAQIDHp2oP2/tMm4Pch/hyjOkwW5RU1AkiWuX21aHH7JhYvzmRCmOdkDz7Yky+/TZ4sH8ppsEXvwICFm/8o0ISy5mnBmc+TTseFD6bfE5z2yD454PK+g4zpbNB3v3S4LaIVRkPQeAnP2BvyIrDean1bR4JY0PWSitkeLvR+nuvnRsVMIc/Rpr/s4p0FIa5ikUBI7E3kO/FYIzIvcm+PTgjsuGPEH/AhQVP8pUtASqYbEHHO0RcB+r/g87fvqvXrZr61KYEUvmwnk0u9sR+4K+AbcCxItmrK/yad1buyYDUc4O6BXAf1HqzEKN+bZXpDralQ/N2IaiisFAFU4L04203BDaXE0KYGlC1NZB/P4DqYTMB+Zdb2LigMX0iQWdZDTZLRxtqh3qU5CO5DfLlqDhrcyzuRMfy2PcRct+xDSQAPvrvrZ18ZYk9jCc3x6d9v4QDB2L8k4sarPVYYsTJzpFqMLNbz7xIm2LVQhJQawfBhPz+pqtKDIWsqPcNinGTT/0L2B35AK6XloljToQWssxIz+XtG11YXWttYb8hS3AniKLa15gowUIJZ3KLsaiszLeEigSv7BF8Oj8XFRFTBM3RANhqBw0dyN8Bm/Qi0NHazD0fGOfdClge/s0WczHcJwwRMFiaHdZ1n1LrwjhQqCSsUM='
parseVote(payload=vote)