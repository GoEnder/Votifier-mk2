import simplejson as json
import socket
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.Hash import SHA, SHA256
import base64
import time
import os

#
# This is example code on how to send a vote to Votifier-mk2
# Votes cosist of a json encoded hash with the values
# Type, serviceName, username, address, timestamp, uuid
# All extra values will be ignored by Votifier-mk2
#
# The Json encoded hash (Our vote) is then signed
# The signature is then appended to the end of the vote string with '\xa7' as a delimiter
# vote + '\xa7' + signature
# And finally sent to the server
#

domain = ''
keyname = 'id_servlist'

def signVote(private, message):
  """ Generates a signature for the vote message """
  rsakey = RSA.importKey(private) 
  signer = PKCS1_v1_5.new(rsakey) 
  digest = SHA256.new() 
  digest.update(message) 
  sign = base64.b64encode(signer.sign(digest))
  return sign

def generateVote(user, addr):
  """ Creates the vote off of information given """
  epoch = time.time()
  uuid = SHA.new("%s%s%s%s%s" % (epoch,domain,os.urandom(25),user,addr)).hexdigest() # Generates a random UUID - This can be anything
  return json.dumps(dict(Type="VOTE", serviceName=domain, username=user, address=addr, timestamp=epoch, uuid=uuid))

def prepareVote(user, addr):
  """ Calls Generate vote, opens your keyfile, 
      and then signs the vote with they key 
  """
  vote = generateVote(user, addr)
  f = open(keyname, 'r').read()
  sign = signVote(f, vote)
  message = vote + '\xa7' + sign
  return message

def sendVote(server, port, user, addr):
  """ Sends the vote off to the server with a bit of redundancy for blocked ports """
  message = prepareVote(user, addr)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(8)
  try:
    s.connect((server, int(port)))
  except:
    try:
      s.close()
    except:
      pass
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(8)
    s.connect((server, int(port)))
  s.send(message)


sendVote(server='127.0.0.1', port='35566', user='KsaRedFx', addr='192.168.0.1')