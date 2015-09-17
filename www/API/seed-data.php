<?php

$conn1 = rand(1,200);
$conn2 = rand(1,200);
$conn3 = rand(1,200);

$array_node_1 = array("name" => "Luxembough", "blocks" => "2551234", "difficulty" => "1234567891234", "connections" => $conn1, "nethashrate" => "1234567891234");
$array_node_2 = array("name" => "Iceland 1", "blocks" => "2551234", "difficulty" => "1234567891234", "connections" => $conn2, "nethashrate" => "1234567891234");
$array_node_3 = array("name" => "Iceland 2", "blocks" => "2551234", "difficulty" => "1234567891234", "connections" => $conn3, "nethashrate" => "1234567891234");

$data[] = $array_node_1;
$data[] = $array_node_2;
$data[] = $array_node_3;

$json_data = json_encode($data);
echo($json_data);

?>