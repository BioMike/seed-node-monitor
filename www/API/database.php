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
	    $this->db->exec("CREATE TABLE seeds (ip_address TEXT UNIQUE, password TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty REAL, nethashrate INTEGER)");
	    //$now = time();
	    //$this->db->exec("INSERT INTO seeds (ip_address, password, timepoint, blocks, connections, difficulty, nethashrate) VALUES ('127.0.0.1', 'pre-Shared secret abcdefghijklmn', $now, 0, 0, 0, 0)");
	    }
	}

    function __destruct()
	{
	$this->db->close();
	}

    function update_node($ip_address, $blocks, $conn, $diff, $nethashrate)
	{
	$now = time();
	$this->db->exec("UPDATE seeds SET blocks=$blocks, connections=$conn, difficulty=$diff, nethashrate=$nethashrate, timepoint=$now WHERE ip_address=$ip_address LIMIT 1");
	}

    function get_password($ip_address)
	{
	$stmt = $this->db->prepare("SELECT password FROM seeds WHERE ip_address=:ip LIMIT 1");
	$status = $stmt->bindValue(':ip', $ip_address, SQLITE3_TEXT);
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
    }
?>