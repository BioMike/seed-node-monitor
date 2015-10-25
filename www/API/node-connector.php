<?php
//    seed-node-monitor: a monitor system for cryptocurrency seed nodes
//    Copyright (C) 2015  Myckel Habets
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU Affero General Public License as published
//    by the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.


include("database.php");
include("hooks/slack_hook.php");

// Settings
// $location is where the database is stored. Store it outside the document tree.
$location = './seeds/';

$db = new Database($location);

// The seed node ip address is a determinant for its data.
$ip_address = $_SERVER['REMOTE_ADDR'];

// Get the data
$iv_post = $_POST['iv'];
$msg_post = $_POST['msg'];

$password = $db->get_password($ip_address);
if(!$password)
    {
    // Node not found.
    die();
    }
$key = mb_convert_encoding($password, "UTF-8");

$iv = base64_decode($iv_post, true);
$msg = base64_decode($msg_post, true);

if($iv && $msg)
    {
    // MCRYPT_RIJNDAEL_128, we use a 16 bit key.
    $json_data = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $msg, MCRYPT_MODE_CBC, $iv);

    $data = json_decode(ltrim($json_data), true);

    $db->update_node($ip_address, $data['blocks'], $data['connections'], $data['difficulty'], $data['nethashrate']);
    }

$offline_nodes = $db->get_offline_nodes();
if(count($offline_nodes) > 0)
    {
    $timeout = $db->get_conf("hooks-slack-timeout");
    if($timeout < time())
	{
	// Run Slack webhook.
	foreach($offline_nodes as $name)
	    {
	    $message = "Seed node $name seems to be offline.";
	    slack_send($message);
	    }
	// Update the timeout, 1 hour.
	$to_till = time() + 60*60;
	$db->set_conf("hooks-slack-timeout", $to_till);
	}
    }

?>