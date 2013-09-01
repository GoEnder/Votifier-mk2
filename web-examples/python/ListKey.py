import simplejson as json
import urllib2
import urllib
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.Hash import SHA256 
import base64

class ListKey(object):
  """
  Example Python Script for a Server List website to push their key to a central listing
  Only should be run after GenerateKey type operations

  'List Key' sends a request that your Public Key is listed in the Central Key Database, and made avaliable to Minecraft Servers

  This is a operation that requires multiple payloads of data sent between the Server List website and the Central Key Database to make sure the keys are 100% valid
  """

  def __init__(self):
    ####
    # Configuration

    # Important Variable to be set correctly 
    self.domain = 'Meow.org' # This must be your domain name without a leading http:// or trailing slashes
    self.detail = '' # This is a quick, one line description of your Server List website

    # Optional Variables below
    # These are best left as-is
    self.keyname = 'servlist'

  def encryptAndSign(self, private, message):
    privkey = RSA.importKey(private) 
    rsakey = PKCS1_OAEP.new(privkey) 
    encrypted = rsakey.encrypt(message) 
    enc_message = encrypted.encode('base64')
    signer = PKCS1_v1_5.new(privkey) 
    digest = SHA256.new(base64.b64decode(enc_message)) 
    sign = signer.sign(digest) 
    return base64.b64encode(sign)

  def decryptMessage(self, private, message):
    rsakey = RSA.importKey(private) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    decrypted = rsakey.decrypt(base64.b64decode(message)) 
    return decrypted

  def loadKeys(self):
    priv = open('id_%s' % self.keyname, 'r')
    priv = priv.read()
    priv = RSA.importKey(priv)
    ssh_rsa = '00000007' + base64.b16encode('ssh-rsa')                                                                                                                                                       
    exponent = '%x' % (priv.e, )
    if len(exponent) % 2:
        exponent = '0' + exponent
    ssh_rsa += '%08x' % (len(exponent) / 2, )
    ssh_rsa += exponent
    modulus = '%x' % (priv.n, )
    if len(modulus) % 2:
        modulus = '0' + modulus
    if modulus[0] in '89abcdef':
        modulus = '00' + modulus
    ssh_rsa += '%08x' % (len(modulus) / 2, )
    ssh_rsa += modulus
    self.id_pub = 'ssh-rsa %s %s' % (base64.b64encode(base64.b16decode(ssh_rsa.upper())), self.domain)
    self.id_priv = priv.exportKey()

  def sendRequest(self):
    payload = json.dumps(dict(list_detail=self.detail, list_domain=self.domain, list_public=self.id_pub))
    url = 'http://127.0.0.1:8834/api/list.json'
    try:
      request = urllib2.Request(url)
      request = urllib2.urlopen(request)
      request.read()
    except Exception as e:
      print """
      Unable to reach Central Key Repository
      %s
      """ % e
      return False
    headers = {"Content-Type":"application/json"}
    request = urllib2.Request(url, payload, headers)
    self.reply = urllib2.urlopen(request)

  def getSecret(self):
    reply = json.loads(self.reply.read())
    message = reply['message']
    token = reply['token']
    url = reply['url']
    print self.decryptMessage(self.id_priv, message)

  def sendSecret(self):
    pass

  def getResult(self):
    pass

  def start(self):
    domain = self.domain
    if (domain == '') or ('/' in domain) or ('.' not in domain):
      print """
      Please include just your domain name in the default configuration of this script, do not include http or trailing slashes
      Good: domain.com
      Bad: http://domain.com/
      """
      return
    self.loadKeys()
    if not self.sendRequest() == False:
      self.getSecret()


ListKey().start()