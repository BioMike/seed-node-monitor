# seed-node-monitor
Monitoring system for crypto currency seed nodes

Work in progress, not tested and doesn't work yet.


##Installation of data collecting software

###Requirements:
* Python 3
* python-bitcoinrpc: Supplied with source in case not available system wide

###Instructions:
1. Change the settings in node-request.py to reflect the coin daemon settings (var: rpc_*).
2. Change the settings in node-request.py to contain the API password (var: secret).
3. As a test, run node-info.py (If everything is correct the data should be updated on the seed monitor webpage).
4. Install a crontab to execute it node-info.puy script every x minutes.

###Crontab
The following crontab setting executes node-request.py every minute:

`*/1 * * * * /location/to/node-request.py`


##Installation of the web and API software

###Requirements:
* A webserver supporting PHP
* PHP version 5.3 or higher, with support of Sqlite 3

###Instructions:
1. Make a folder outside the webserver document root tree, but writable by the webserver.
2. Copy the contents of the www folder into the document root tree.
3. Change API/node-collector.php to point the location to the folder in point 1 (var: $location).
4. Generate some passwords with the pw-gen.py script in utils.
5. Open API/database.php and change the lines (line 25 and 26 as example) for creating the database.
