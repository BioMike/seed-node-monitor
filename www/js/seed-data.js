function init() {

    $.get( "/API/seed-data.php", function( data ) {
	for(var i = 0; i < data.length, i++)
	    {
	    var node = data[i];
	    var node_element = document.createElement("div");
	    // name
	    var name_element = document.createElement("div");
	    name_element.appendChild(document.createTextNode(node["name"]));
	    node_element.appendChild(name_element);
	    // blocks
	    var blocks_element = document.createElement("div");
	    blocks_element.appendChild(document.createTextNode(node["blocks"]));
	    node_element.appendChild(blocks_element);
	    // conn
	    var conn_element = document.createElement("div");
	    conn_element.appendChild(document.createTextNode(node["connections"]));
	    node_element.appendChild(conn_element);
	    // diff
	    // nethashrate
	    document.getElementById('nodelist').appendChild(node_element);
	    }
};