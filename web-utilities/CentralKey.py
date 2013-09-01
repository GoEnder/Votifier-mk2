from Crypto.PublicKey import RSA
import os


def genKey():
  key = RSA.generate(4096, os.urandom)
  id_priv = key.exportKey()
  id_pub = key.publickey().exportKey('OpenSSH')
  print "%s - %s" % (id_priv, id_pub)


genKey()