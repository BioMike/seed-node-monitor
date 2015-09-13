<?php
include("database.php");

// Settings
// $location is where the database is stored. Store it outside the document tree.
$location = './seeds/';

$db = Database($location);

// The seed node ip address is a determinant for its data.
$ip_address = $_SERVER['REMOTE_ADDR'];

// Get the data
$iv = $_POST['iv'];
$msg = $_POST['msg'];

$password = $db->get_password($ip_address);
if(!$password)
    {
    // Node not found.
    die();
    }
$key = mb_convert_encoding($password, "UTF-8");

// MCRYPT_RIJNDAEL_128, we use a 16 bit key.
$json_data = mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, base64_decode($msg), MCRYPT_MODE_CBC, base64_decode($iv));

$data = json_decode(ltrim($json_data));

$db->update_node($ip_address, $data['blocks'], $data['connections'], $data['difficulty'], $data['$nethashrate']);

?>