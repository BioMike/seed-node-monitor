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