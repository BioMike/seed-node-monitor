function init() {

   $.get( "/API/seed-data.php", function( data ) {
   alert( "Data Loaded: " + data );
   });
};