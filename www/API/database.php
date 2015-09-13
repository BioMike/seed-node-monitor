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
	$this->db = sqlite_open($filename);
	
	// Create the seeds table if the file didn't exist.
	// Note no seeds are inserted here by default. Uncomment/Edit below to define nodes that should be added to the system.
	if($db_new)
	    {
	    sqlite_exec($this->db, "CREATE TABLE seeds (ip_address TEXT UNIQUE, password TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty REAL, nethashrate INTEGER)");
	    //$now = time();
	    //sqlite_exec($this->db, "INSERT INTO seeds (ip_address, password, timepoint, blocks, connections, difficulty, nethashrate) VALUES ('127.0.0.1', 'pre-Shared secret abcdefghijklmn', $now, 0, 0, 0, 0)");
	    }
	}

    function __descruct()
	{
	sqlite_close($his->db);
	}

    function update_node($ip_address, $blocks, $conn, $diff, $nethashrate)
	{
	$now = time();
	sqlite_exec($this->db, "UPDATE seeds SET blocks=$blocks, connections=$conn, difficulty=$diff, nethashrate=$nethashrate, timepoint=$now WHERE ip_address=$ip_address LIMIT 1");
	}

    function get_password($ip_address)
	{
	$res = sqlite_query($this->db, "SELECT password FROM seeds where ip_address=$ip_address LIMIT 1");
	if(sqlite_num_rows($res) > 0)
	    {
	    $retval = sqlite_fetch_single($res);
	    }
	    else
	    {
	    $retval = false;
	    }
	return($retval);
	}
    }
?>