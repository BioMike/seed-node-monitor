<?php
class Database
    {
    function __construct($location)
	{
	// Check if database exists.
	$filename = $location . "seednodes.db";
	if(file_exists($filename))
	    {
	    $db_new = false;
	    }
	    else
	    {
	    $db_new = true;
	    }
	
	// Open the database.
	$this->db = new SQLite3($filename);
	
	// Create the seeds table if the file didn't exist.
	// Note no seeds are inserted here by default. Uncomment/Edit below to define nodes that should be added to the system.
	if($db_new)
	    {
	    $this->db->exec("CREATE TABLE seeds (ip_address TEXT UNIQUE, password TEXT, name TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty REAL, nethashrate INTEGER)");
	    //$now = time();
	    //$this->db->exec("INSERT INTO seeds (ip_address, password, timepoint, blocks, connections, difficulty, nethashrate) VALUES ('127.0.0.1', 'pre-Shared secret abcdefghijklmn', 'Home', $now, 0, 0, 0, 0)");
	    }
	}

    function __destruct()
	{
	$this->db->close();
	}

    function update_node($ip_address, $blocks, $conn, $diff, $nethashrate)
	{
	$now = time();
	$stmt = $this->db->prepare("UPDATE seeds SET blocks=:blocks, connections=:conn, difficulty=:diff, nethashrate=:nhr, timepoint=:now WHERE ip_address=:ip");
	$stmt->bindValue(':ip', $ip_address, SQLITE3_TEXT);
	$stmt->bindValue(':blocks', $blocks, SQLITE3_INTEGER);
	$stmt->bindValue(':conn', $conn, SQLITE3_INTEGER);
	$stmt->bindValue(':diff', $diff);
	$stmt->bindValue(':nhr', $nethashrate, SQLITE3_INTEGER);
	$stmt->bindValue(':now', $now, SQLITE3_INTEGER);
	$result = $stmt->execute();
	}

    function get_password($ip_address)
	{
	$stmt = $this->db->prepare("SELECT password FROM seeds WHERE ip_address=:ip LIMIT 1");
	$stmt->bindValue(':ip', $ip_address, SQLITE3_TEXT);
	$result = $stmt->execute();
	if($result->numColumns())
	    {
	    $result->reset();
	    $data = $result->fetchArray();
	    $retval = $data[0];
	    }
	    else
	    {
	    $retval = false;
	    }
	return($retval);
	}

    function get_seeds_data()
	{
	$return_data = array();
	$stmt = $this->db->prepare("SELECT name, timepoint, blocks, connections, difficulty, nethashrate FROM seeds");
	$result = $stmt->execute();
	while($data = $result->fetchArray(SQLITE3_ASSOC))
	    {
	    $return_data[] = $data;
	    }
	return($return_data);
	}
    }
?>