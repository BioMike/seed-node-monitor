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
	
	// Create the seeds table if the database file didn't exist.
	// People should use the util/db-util.py tool to add seed nodes to it.
	if($db_new)
	    {
	    $this->db->exec("CREATE TABLE seeds (ip_address TEXT UNIQUE, password TEXT, name TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty REAL, nethashrate INTEGER)");
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

    function get_offline_nodes()
	{
	// Get nodes that haven't connected in 5 minutes.
	$timed_out = time() - 5*60;
	$return_data = array();
	$stmt = $this->db->prepare("SELECT name FROM seeds WHERE timepoint<:timedout");
	$stmt->bindValue(':timedout', $timed_out, SQLITE3_INTEGER);
	$result = $stmt->execute();
	while($data = $result->fetchArray(SQLITE3_ASSOC))
	    {
	    $return_data[] = $data;
	    }
	return($return_data);
	}

   function get_conf($confkey)
	{
	$stmt = $this->db->prepare("SELECT confval FROM config WHERE confkey=:confkey LIMIT 1");
	$stmt->bindValue(':confkey', $confkey, SQLITE3_TEXT);
	$result = $stmt->execute();
	$data = $result->fetchArray(SQLITE3_ASSOC);
	}

    function set_conf($confkey, $confval)
	{
	$stmt = $this->db->prepare("UPDATE config SET confval=:confval WHERE confkey=:confkey");
	$stmt->bindValue(':confval', $confval, SQLITE3_TEXT);
	$stmt->bindValue(':confkey', $confkey, SQLITE3_TEXT);
	$result = $stmt->execute();
	}
    }
?>