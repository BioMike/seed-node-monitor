import json
from Crypto.Cipher import AES
from Crypto import Random
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Base settings

# Settings, change them here

secret = 'pre-Shared secret' # 32 characters
rpc_user = ''
rpc_password = ''
rpc_host = '127.0.0.1'
rpc_port = '12340'

# Settings, most likely not to change them
monitor_host = ''

# Connecting to node
rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_host, rpc_port))

# Collect data
nodeinfo = rpc_connection.getinfo()
networkhps = rpc_connection.getnetworkhashps()

# Build JSON object
print(nodeinfo)
print(networkhps)
json_data = json.dumps(data)

# Encrypt it
key = bytearray(secret, 'utf-8')
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
msg = iv + cipher.encrypt(bytearray(json_data, 'utf-8'))

# Send to the collecting server