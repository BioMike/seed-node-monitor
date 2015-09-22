/*
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
*/

function init() {
 $(document).ready(function() {
   reload_data();
   var timerId = setInterval(function() {
	reload_data();
   }, 5000);
});

};

function reload_data() {
    $.ajaxSetup({ cache: false });
    $.get( "/API/seed-data.php", function( data ) {
        var nodelist = $( "#nodelist" );
        nodelist.empty();
	$(jQuery.parseJSON(data)).each(function() {
	    
	    var name = this.name;
	    var blocks = this.blocks;
	    var conn = this.connections;
	    var diff = this.difficulty;
	    var nhr = this.nethashrate;

	    var node_element = $( "<div />" );
	    node_element.addClass("node-entry");
	    // name
	    var name_element = $( "<div />" );
	    name_element.addClass("node-name");
	    name_element.append(name);
	    node_element.append(name_element);
	    // blocks
	    var blocks_element = $( "<div />" );
	    blocks_element.addClass("node-blocks");
	    blocks_element.append(blocks);
	    node_element.append(blocks_element);
	    // conn
	    var conn_element = $( "<div />" );
	    conn_element.addClass("node-conn");
	    conn_element.append(conn);
	    node_element.append(conn_element);
	    // diff
	    var diff_element = $( "<div />" );
	    diff_element.addClass("node-diff");
	    diff_element.append(diff);
	    node_element.append(diff_element);
	    // nethashrate
	    var nhr_element = $( "<div />" );
	    nhr_element.addClass("node-conn");
	    nhr_element.append(nhr);
	    node_element.append(nhr_element);

	    nodelist.append(node_element);
	    });
	});
    };