<?php
include("database.php");

// Settings
// $location is where the database is stored. Store it outside the document tree.
$location = './seeds/';

$db = new Database($location);

$data = $db->get_seeds_data();

$json_data = json_encode($data);
echo($json_data);

?>