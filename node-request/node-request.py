import json
import random
import base64
import urllib
import urllib2

from Crypto.Cipher import AES
from Crypto import Random
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Base settings
# Settings, change them here

secret = 'pre-Shared secret abcdefghijklmn' # 32 characters

rpc_user = 'auroracoinrpc'
rpc_password = ''
rpc_host = '127.0.0.1'
rpc_port = '12341'

# Settings, most likely not to change them
monitor_url = 'http://seeds.auroracoin.is/API/node-connector.php'

# Connecting to node
rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_host, rpc_port))

# Collect data
nodeinfo = rpc_connection.getinfo()
networkhps = rpc_connection.getnetworkhashps()
difficulty = rpc_connection.getdifficulty()
randomness = random.randint(0, 800000)

# Build JSON object
# {'protocolversion': 2000000, 'errors': '', 'blocks': 157595, 'paytxfee': Decimal('0E-8'), 'keypoolsize': 103, 'walletversion': 60000, 
# 'keypoololdest': 1433533648, 'testnet': False, 'version': 80705, 'connections': 3, 'proxy': '', 'mininput': Decimal('0.00001000'), 
# 'balance': Decimal('0E-8'), 'timeoffset': 0, 'difficulty': Decimal('153.73652958')}
# 2111779983
#print(nodeinfo)
#print(networkhps)
data = {'blocks': nodeinfo['blocks'], 'connections': nodeinfo['connections'], 'difficulty': str(difficulty), 'nethashrate': networkhps, 'random': randomness}
json_data = json.dumps(data)

#print(json_data)

num = int((len(json_data)/AES.block_size) + 1)

# Encrypt it
key = bytes(secret, 'utf-8')
# AES.block_size = 16, which translates to MCRYPT_RIJNDAEL_128 in PHP
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)
msg_iv = base64.b64encode(iv)
msg = base64.b64encode(cipher.encrypt(bytes(json_data.rjust(num * AES.block_size), 'utf-8')))

parameters = {'iv': msg_iv, 'msg': msg}

# Send to the collecting server
#print(msg_iv)
#print(msg)

params = urllib.urlencode(parameters)
req = urllib2.Request(monitor_url, params)
req.add_header("Content-type", "application/x-www-form-urlencoded")
response = urllib2.urlopen(req)

