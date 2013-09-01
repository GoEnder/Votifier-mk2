import os
from Crypto.PublicKey import RSA
import base64

class GenerateKey(object):
  """
  Example Python Script for a Server List website to generate a Private key and Public Key pair in Python
  Only should be run once, or when a Server List comprimization happens
  """

  def __init__(self):
    ####
    # Configuration

    # Important Variable to be set correctly 
    # This must be your domain name without a leading http:// or trailing slashes
    self.domain = 'localhost.com'

    # Optional Variables below
    # These are best left as-is
    self.keysize = 4096
    self.keyname = 'servlist'

  def makeKey(self):
    """Generates the RSA Keypair"""
    key = RSA.generate(self.keysize, os.urandom)
    self.id_priv = key.exportKey()                                                                                                                 
    self.id_pub = "%s %s" % (key.publickey().exportKey('OpenSSH'), self.domain)

  def saveKey(self):
    """Saves the RSA Keypair to file"""
    priv = open('id_%s' % self.keyname, 'w')
    priv.write(self.id_priv)
    priv.close()
    pub = open('id_%s.pub' % self.keyname, 'w')
    pub.write(self.id_pub)
    pub.close()

  def start(self):
    domain = self.domain
    if (domain == '') or ('/' in domain) or ('.' not in domain):
      print """
      Please include just your domain name in the default configuration of this script, do not include http or trailing slashes
      Good: domain.com
      Bad: http://domain.com/
      """
      return
    if self.keysize < 2048:
      self.keysize = 4096
    if (self.keyname == ''):
      self.keyname = 'servlist'
    self.makeKey()
    self.saveKey()

GenerateKey().start()
