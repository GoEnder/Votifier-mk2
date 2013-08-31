import simplejson as json

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
    # This must be your domain name without a leading http:// or trailing slashes
    self.domain = ''

    # Optional Variables below
    # These are best left as-is
    self.keyname = 'servlist'

  def composeRequest(self):
    pass

  def getSecret(self):
    pass

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