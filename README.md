# seed-node-monitor
Monitoring system for crypto currency seed nodes


## Installation of data collecting software

### Requirements:
* Python 3, including requests module
* python-bitcoinrpc: Supplied with source in case not available system wide
* pycrypto

### Ubuntu notes
The requests module is not installed by default on Ubuntu. Use "apt-get install python-pip && pip install requests" to install it.
Ubuntu users should also install the python3-crypto package for pycrypto.

### Instructions:
1. Change the settings in node-request.py to reflect the coin daemon settings (var: rpc_*).
2. Change the settings in node-request.py to contain the API password (var: secret).
3. As a test, run node-request.py (If everything is correct the data should be updated on the seed monitor webpage).
4. Install a crontab to execute it node-request.py script every x minutes.

### Crontab
The following crontab setting executes node-request.py every minute:

`*/1 * * * * /location/to/node-request.py`


## Installation of the web and API software

### Requirements:
* A webserver supporting PHP
* PHP version 7.2 or higher, with support of Sqlite 3

### Instructions:
1. Make a folder outside the webserver document root tree, but writable by the webserver.
2. Copy the contents of the www folder into the document root tree.
3. Change API/node-collector.php and API/seed-data.php files to point the location to the folder in point 1 (var: $location).
4. Create a database with the util/db-util.py program and add nodes to it. (Make sure the database file is in the 
   location of 1, has the name "seednodes.db" and is readable by the webserver.)
