import json
import random
import binascii
from Crypto.Cipher import AES
from Crypto import Random
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Base settings

# Settings, change them here

secret = 'pre-Shared secret abcdefghijklmn' # 32 characters

rpc_user = 'auroracoinrpc'
rpc_password = 'secret'
rpc_host = '127.0.0.1'
rpc_port = '12341'

# Settings, most likely not to change them
monitor_host = ''

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

# Encrypt it
key = bytes(secret, 'utf-8')
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
msg = iv + cipher.encrypt(bytes(json_data, 'utf-8'))

# Send to the collecting server
encoded = binascii.hexlify(msg)
print(msg)
print('\n')
print(encoded)
print('\n')
print(binascii.unhexlify(encoded))