---
id: 1023
title: 'Mapping Oil and Gas Incidents in Alberta: Improvements'
date: 2014-06-25T01:26:35+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=1023
permalink: /2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/
geo_public:
  - "0"
dsq_thread_id:
  - "6140711725"
image: https://everettsprojects.com/wp/wp-content/uploads/2014/06/mapsimproved-672x372.png
categories:
  - Environmental Science
  - Programming
  - Web Applications
tags:
  - AER
  - AJAX
  - Alberta
  - ERCB
  - Google Maps
  - javaScript
  - JQuery
  - MySQL
  - Oil and Gas Incidents
  - Oil Spills
  - PHP
---
**This post is a continuation of the original [Mapping Oil and Gas Incidents in Alberta with Google Maps, JQuery, and PHP](http://everettsprojects.com/2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/) post. If you wish to know more about this project or find the code for version 1, it is suggested you start there.**

<div id="attachment_1033" style="width: 959px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/spills/"><img class="wp-image-1033 size-full" src="http://everett.x10.mx/wp/wp-content/uploads/2014/06/mapsimproved.png" alt="" width="949" height="679" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/06/mapsimproved.png 949w, https://everettsprojects.com/wp/wp-content/uploads/2014/06/mapsimproved-300x214.png 300w" sizes="(max-width: 949px) 100vw, 949px" /></a>
  
  <p class="wp-caption-text">
    The new map, with 100% less marker overlap and all relevant incidents displayed for a selected location.
  </p>
</div>

_If you just want a copy of all the files necessary (minus the database), then I have them both on [github](https://github.com/evjrob/Alberta-Spills-Map) or in a [zipped archive](http://everett.x10.mx/spills/spills.zip). Don&#8217;t forget to go in and change the values of config.inc.php to reflect your own MySQL database. If you would like the original ver. 1 source code, please check the [original post](http://everettsprojects.com/2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/ "Mapping Oil and Gas Incidents in Alberta with Google Maps, JQuery, and PHP")._

Developing software is a never-ending process. There&#8217;s always a bug to fix, a feature that should have been included, and a better way of doing the same thing. The first version of this project had a number of issues that I had identified. There are still the issues related to the data; that only incidents falling under the jurisdiction of the ERCB/AER are included, and that plotted incident locations are only accurate to +/-200m in each axis. The related issue of multiple incidents being plotted on top of each other and difficult to select without extensive filter use is now fixed though. All incidents for a given ATS Legal Subdivision and the applied filters are now returned and listed in the _Incident Details_ panel, along with a small indication of the number of incidents that have been selected.

The final issue; three points in the South Atlantic Ocean are still there, and the multiple incidents per map marker feature that has been implemented doesn&#8217;t work with them. This is because they are still being plotted on the map using latitude and longitude, but the incident info selection process works based on the Alberta Township System location. While these points all share a latitude and longitude of 0,0 their ATS locations are different, and so the problem of overlapping markers still exists here.

In addition to these issues identified for the original write-up, it also came to my attention that there was a problem with the way the page rendered on iPads. This was easily fixed by switching the width scale of the info-panel <div> element to be based upon the &#8220;em&#8221; unit instead of % as it originally was. By having the width of the feature be based on a fundamentally text oriented unit, the rendering has actually been made more consistent across all devices.

<p style="text-align:center;">
   *****
</p>

Lets take a closer look at the most major change; fixing the overlapping markers issue started with identifying the ATS location for each map marker as the preferred identifier over the Incident Number. Since we are now selecting database entries using the Location column in the database, it makes sense to add an index to this column:

[code language=&#8221;sql&#8221;]
  
ALTER TABLE \`Spills\` ADD INDEX( \`Location\` );
  
[/code]

The getSpillInfo.php file also needs to be updated to reflect these changes. It now no longer just fetches the info for a specific unique Incident Number, it needs to fetch all the results for a given ATS location and the filter parameters set:

[code language=&#8221;php&#8221; title=&#8221;getSpillInfo.php&#8221;]
  
<?php
  
require(&#8216;config.inc.php&#8217;);

$atsLocation = $_POST[&#8216;Location&#8217;];
  
$currentlicensee = $_POST[&#8216;currentLicensee&#8217;];
  
$currentsubstance = $_POST[&#8216;currentSubstance&#8217;];
  
$currentsource = $_POST[&#8216;currentSource&#8217;];
  
$yearmin = $_POST[&#8216;yearMin&#8217;];
  
$yearmax = $_POST[&#8216;yearMax&#8217;];
  
$volumemin = $_POST[&#8216;volumeMin&#8217;];
  
$volumemax = $_POST[&#8216;volumeMax&#8217;];

// Fix the years to go from start of first year to end of the last.
  
$datemin = $yearmin."-01-01";
  
$datemax = $yearmax."-12-31";

//By using PDO and prepare, everything is automagically escaped
  
$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);

//Start building the statement with the base of the query
  
$stmtString = "SELECT * FROM \`Spills\` WHERE (\`Location\` = :ATSLocation AND (\`IncidentDate\` BETWEEN :dateMin AND :dateMax) AND (\`Volume Released\` BETWEEN :volumeMin AND :volumeMax)";

//Add in the filters if they&#8217;re set
  
if ($currentlicensee !== "All") {
   
$stmtString .= " AND \`LicenseeName\` = :licensee";
  
}
  
if ($currentsubstance !== "All") {
   
$stmtString .= " AND \`Substance Released\` = :substance";
  
}
  
if ($currentsource !== "All") {
   
$stmtString .= " AND \`Source\` = :source";
  
}

//Finish the statement with the sorting part
  
$stmtString .= ") ORDER BY \`IncidentDate\` DESC";

//Bind all of the parameters
  
$stmt = $db->prepare($stmtString);
  
if (strpos($stmtString,&#8217;:licensee&#8217;) !== false) {
   
$stmt->bindValue(&#8216;:licensee&#8217;, strval($currentlicensee), PDO::PARAM_STR);
  
}
  
if (strpos($stmtString,&#8217;:source&#8217;) !== false) {
   
$stmt->bindValue(&#8216;:source&#8217;, strval($currentsource), PDO::PARAM_STR);
  
}
  
if (strpos($stmtString,&#8217;:substance&#8217;) !== false) {
   
$stmt->bindValue(&#8216;:substance&#8217;, strval($currentsubstance), PDO::PARAM_STR);
  
}
  
$stmt->bindValue(&#8216;:dateMin&#8217;, strval($datemin), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:dateMax&#8217;, strval($datemax), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:volumeMin&#8217;, strval($volumemin), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:volumeMax&#8217;, strval($volumemax), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:ATSLocation&#8217;, strval($atsLocation), PDO::PARAM_STR);
  
$stmt->execute();

//Get the results of the query
  
$result;
  
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo header(&#8216;Content-type: application/json&#8217;);
  
echo json_encode($result);

?>
  
[/code]

With the ATS location being the primary selection parameter, we&#8217;ll also need to update the getSpillLocations.php file to reflect this. Namely line 25, where the \`Location\` column has been added to the SELECT statement, and required to be distinct as well. This will ensure we are provided up to 100 unique legal subdivisions containing the largest single (non-cumulative) incidents for the current map view port:

[code language=&#8221;php&#8221; title=&#8221;getSpillLocations.php&#8221;]
  
<?php
  
require(&#8216;config.inc.php&#8217;);

//Get all of the POST data
  
$currentlicensee = $_POST[&#8216;currentLicensee&#8217;];
  
$currentsubstance = $_POST[&#8216;currentSubstance&#8217;];
  
$currentsource = $_POST[&#8216;currentSource&#8217;];
  
$yearmin = $_POST[&#8216;yearMin&#8217;];
  
$yearmax = $_POST[&#8216;yearMax&#8217;];
  
$volumemin = $_POST[&#8216;volumeMin&#8217;];
  
$volumemax = $_POST[&#8216;volumeMax&#8217;];
  
$latmin = $_POST[&#8216;latMin&#8217;];
  
$latmax = $_POST[&#8216;latMax&#8217;];
  
$longmin = $_POST[&#8216;lngMin&#8217;];
  
$longmax = $_POST[&#8216;lngMax&#8217;];

// Fix the years to go from start of first year to end of the last.
  
$datemin = $yearmin."-01-01";
  
$datemax = $yearmax."-12-31";

//By using PDO and prepare, everything is automagically escaped
  
$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);

//Start building the statement with the base of the query
  
$stmtString = "SELECT DISTINCT(\`Location\`), \`Latitude\`, \`Longitude\` FROM \`Spills\` WHERE (((\`Longitude\` BETWEEN :longMin AND :longMax) AND (\`Latitude\` BETWEEN :latMin AND :latMax) AND (\`IncidentDate\` BETWEEN :dateMin AND :dateMax) AND (\`Volume Released\` BETWEEN :volumeMin AND :volumeMax))";

//Add in the filters if they&#8217;re set
  
if ($currentlicensee !== "All") {
   
$stmtString .= " AND \`LicenseeName\` = :licensee";
  
}
  
if ($currentsubstance !== "All") {
   
$stmtString .= " AND \`Substance Released\` = :substance";
  
}
  
if ($currentsource !== "All") {
   
$stmtString .= " AND \`Source\` = :source";
  
}

//Finish the statement with the sorting and limit parts
  
$stmtString .= ") ORDER BY \`Volume Released\` DESC LIMIT 100";

//Bind all of the parameters
  
$stmt = $db->prepare($stmtString);
  
if (strpos($stmtString,&#8217;:licensee&#8217;) !== false) {
   
$stmt->bindValue(&#8216;:licensee&#8217;, strval($currentlicensee), PDO::PARAM_STR);
  
}
  
if (strpos($stmtString,&#8217;:source&#8217;) !== false) {
   
$stmt->bindValue(&#8216;:source&#8217;, strval($currentsource), PDO::PARAM_STR);
  
}
  
if (strpos($stmtString,&#8217;:substance&#8217;) !== false) {
   
$stmt->bindValue(&#8216;:substance&#8217;, strval($currentsubstance), PDO::PARAM_STR);
  
}
  
$stmt->bindValue(&#8216;:latMin&#8217;, strval($latmin), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:latMax&#8217;, strval($latmax), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:longMin&#8217;, strval($longmin), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:longMax&#8217;, strval($longmax), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:dateMin&#8217;, strval($datemin), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:dateMax&#8217;, strval($datemax), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:volumeMin&#8217;, strval($volumemin), PDO::PARAM_STR);
  
$stmt->bindValue(&#8216;:volumeMax&#8217;, strval($volumemax), PDO::PARAM_STR);
  
$stmt->execute();

//Get the results of the query
  
$result;
  
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
  
//Spit out the results in json form
  
echo header(&#8216;Content-type: application/json&#8217;);
  
echo json_encode($result);
  
?>
  
[/code]

Now the index.html file needs to be updated to reflect these changes. This starts with the spillID attributes of the map marker objects being replaced with ATS Location, the plotSpills() function being modified to not duplicate markers when one already exists for that LSD, the loadSpillInfo() function being modified to use the ATS location, then finally populate the Incident Details panel with a &#8220;Number of incidents selected&#8221; count and a table for each of these incidents.

[code language=&#8221;javascript&#8221; htmlscript=&#8221;true&#8221; title=&#8221;index.html&#8221;]
  
<!DOCTYPE html>
  
<html>
      
<head>
          
<meta name="viewport" content="initial-scale=1.0">
          
<meta charset="utf-8">
          
<title>Alberta Oil and Gas Incidents 1975 &#8211; 2013</title>
          
<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
          
<link href="default.css" rel="stylesheet">
          
<!&#8211; Google Analytics &#8211;>
	  
<script>
	    
(function(i,s,o,g,r,a,m){i[&#8216;GoogleAnalyticsObject&#8217;]=r;i[r]=i[r]||function(){
	    
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	    
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	    
})(window,document,&#8217;script&#8217;,&#8217;//www.google-analytics.com/analytics.js&#8217;,&#8217;ga&#8217;);

ga(&#8216;create&#8217;, &#8216;UA-51737914-1&#8217;, &#8216;x10.mx&#8217;);
	    
ga(&#8216;send&#8217;, &#8216;pageview&#8217;);

</script>
	  
<!&#8211; End Google Analytics &#8211;>
          
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
          
<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
          
<script type="text/javascript"
              
src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCIxpXOSPJWNG7TnhMYq-Q2hPcM7zEQs8g&sensor=false">
          
</script>
          
<script>
              
//Make a bunch of variables to track the filters and map boundaries
              
var sqlParameters = {
                  
currentSubstance : &#8216;All&#8217;,
                  
currentSource : &#8216;All&#8217;,
                  
currentLicensee: &#8216;All&#8217;,
                  
yearMin : 1975,
                  
yearMax : 2013,
                  
volumeMin : 0,
                  
volumeMax : 37000000,
                  
latMin : 0,
                  
latMax : 0,
                  
lngMin : 0,
                  
lngMax : 0
              
}

/////////////////////////////////////
              
//Nice control widgets from jQueryUI:
              
/////////////////////////////////////

//Popup dialog window for disclaimer
              
$(function() {
                  
$( "#disclaimer" ).dialog({
                      
autoOpen: false
                  
});

$( "#disclaimer-opener" ).click(function() {
                      
$( "#disclaimer" ).dialog( "open" );
                  
});
              
});

//Popup dialog window for license
              
$(function() {
                  
$( "#license" ).dialog({
                      
autoOpen: false,
                      
width: 350
                  
});

$( "#license-opener" ).click(function() {
                      
$( "#license" ).dialog( "open" );
                  
});
              
});

//No data fetched dialog
              
$(function() {
                  
$("#no-data").dialog({
                      
height: 80,
                      
autoOpen: false,
                      
dialogClass: &#8216;noTitleDialog&#8217;,
                      
open: function(event, ui){
                          
setTimeout("$(&#8216;#no-data&#8217;).dialog(&#8216;close&#8217;)",3000);
                      
}
                  
});
              
});

//Sliders
              
$(function () {
                  
$(".slider").each(function () {
                      
var begin = $(this).data("begin"),
                          
end = $(this).data("end"),
                          
step = $(this).data("step");

$(this).slider({
                          
range: "true",
                          
values: [begin, end],
                          
min: begin,
                          
max: end,
                          
step: step,
                          
slide: function (event, ui) {
                              
//Update text box quantity when the slider changes
                              
var sliderlow = ("#" + $(this).attr("id") + "\_amount\_low");
                              
$(sliderlow).val(ui.values[0]);

var sliderhigh = ("#" + $(this).attr("id") + "\_amount\_high");
                              
$(sliderhigh).val(ui.values[1]);
                          
},
                          
//When the slider changes, update the displayed spills
                          
change: function(event, ui) {
                              
if ($(this).attr("id") == "years") {
                                  
sqlParameters.yearMin = ui.values[0];
                                  
sqlParameters.yearMax = ui.values[1];
                              
} else if ($(this).attr("id") == "volume") {
                                  
sqlParameters.volumeMin = ui.values[0];
                                  
sqlParameters.volumeMax = ui.values[1];
                              
}
                              
getSpills();
                          
}
                      
})

//Initialize the text box quantity
                      
var sliderlow = ("#" + $(this).attr("id") + "\_amount\_low");
                      
$(sliderlow).val($(this).slider("values", 0));

var sliderhigh = ("#" + $(this).attr("id") + "\_amount\_high");
                      
$(sliderhigh).val($(this).slider("values", 1));
                  
})

//When the text box is changed, update the slider
                  
$(&#8216;.amount1&#8217;).change(function () {
                      
var value = this.value,
                      
selector = $("#" + this.id.split(&#8216;_&#8217;)[0]);
                      
selector.slider("values", 0, value);
                  
})
                  
$(&#8216;.amount2&#8217;).change(function () {
                      
var value = this.value,
                      
selector = $("#" + this.id.split(&#8216;_&#8217;)[0]);
                      
selector.slider("values", 1, value);
                  
})
              
});

//Accordian divs
              
$(function() {
                  
$( "#accordion" ).accordion({
                      
collapsible: true,
                      
autoHeight: false,
                      
heightStyle: "content"
                  
});
              
});

//Get the Licensee list for the autocomplete widget
              
var licenseeList = [];
              
$.ajax({
                  
async: false,
                  
url : "getLicensees.php",
                  
dataType : "json",
                  
success: function(data){
                      
licenseeList = data;
                  
},
                  
error: function (data)
                  
{
                      
alert("Couldn&#8217;t retrieve the licensee list. A page refresh will usually fix this.");
                  
}
              
});

//Auto Complete Licensee Selector
              
$(function() {
                  
var cache = [];
                  
$( "#licensee-selector" ).autocomplete({
                      
minLength: 2,
                      
source: licenseeList,
                      
select: function( event, ui ) {
                          
sqlParameters.currentLicensee = ui.item.value;
                          
getSpills();
                      
}
                  
});

$( "#licensee-clear" ).click(function() {
                      
$( "#licensee-selector" ).val("");
                      
sqlParameters.currentLicensee = &#8216;All&#8217;;
                      
getSpills();
                  
});

});

//Drop down menus
              
$(function() {
                  
$( "#substance-menu, #source-menu" ).menu();
              
}); 

//When the DOM is loaded, we want to configure stuff like the menus
              
$( document ).ready(function() {
                  
makeMenus();

//A hackish way to set the spill-info content max height based on window height
                  
document.getElementById("spill-info").style.maxHeight = $(window).height()*0.40 + "px";

});

//Build the menus after the window has loaded (This is called at the end of <body>)
              
function makeMenus() {

//Get the substances and sources for the filter menus
                  
var substanceList = [];
                  
$.ajax({
                      
async: false,
                      
url : "getSubstances.php",
                      
dataType : "json",
                      
success: function(data){
                          
substanceList = data;
                          
//replace the initial null element
                          
substanceList[0] = "All";
                      
},
                      
error: function (data)
                      
{
                          
alert("Couldn&#8217;t retrieve the substance list. A page refresh will usually fix this.");
                      
}
                  
});

//And the Sources too
                  
var sourceList = [];
                  
$.ajax({
                      
async: false,
                      
url : "getSources.php",
                      
dataType : "json",
                      
success: function(data){
                          
sourceList = data;
                          
//replace the initial null element
                          
sourceList[0] = "All";
                      
},
                      
error: function (data)
                      
{
                          
alert("Couldn&#8217;t retrieve the source list. A page refresh will usually fix this.");
                      
}
                  
});

//Build the lists using the database results
                  
//Function courtesy of http://stackoverflow.com/questions/11128700/create-a-ul-and-fill-it-based-on-a-passed-array
                  
function constructLI(domID, array) {

var fieldID = (domID.split("-"))[0]+"-selected";

for(var i = 0; i < array.length; i++) {
                          
// Create the list item:
                          
var member = document.createElement(&#8216;li&#8217;);

// Set its contents:
                          
var linkText = document.createTextNode(array[i]);
                          
var link = document.createElement(&#8216;a&#8217;);
                          
link.appendChild(linkText);
                          
link.href= "#";
                          
link.title= linkText;

//Make the onclick aspect of them menu work
                          
link.onclick = function() { setText( fieldID, this.firstChild.nodeValue ) };

member.appendChild(link);

// Add it to the list:
                          
document.getElementById(domID).appendChild(member);
                      
}
                  
}
                  
constructLI("substance-links", substanceList);
                  
constructLI("source-links", sourceList);
              
}

//Set the drop down menu to reflect the new filter value and update the displayed results
              
function setText(domID, text) {
                  
document.getElementById(domID).innerHTML = text;
                  
if (domID == "substance-selected") {
                      
sqlParameters.currentSubstance = text;
                  
} else if (domID == "source-selected") {
                      
sqlParameters.currentSource = text;
                  
}
                  
getSpills();
              
};

//////////////////////////////
              
//Start the Google Maps stuff
              
//////////////////////////////

var map;
              
var markers = [];
              
var selectedMarker = new google.maps.Marker({
                                  
position: null,
                                  
icon: &#8216;spotlight-poi.png&#8217;,
                                  
map: map,
                                  
ATSLocation: ""
                          
});
              
var spillLocations;

//Initialize when the map is done
              
google.maps.event.addDomListener(window, &#8216;load&#8217;, initialize);

function initialize() { clearStyle: true;
                  
var middleEarth = new google.maps.LatLng(54.5, -115.0);
                  
var mapOptions = {
                      
zoom: 6,
                      
center: middleEarth,
                      
mapTypeId: google.maps.MapTypeId.ROADMAP
                  
};

map = new google.maps.Map(document.getElementById(&#8216;map-canvas&#8217;), mapOptions); 

makeGetSpillsEvent();
              
}

function makeGetSpillsEvent(){
                  
google.maps.event.addListener(map, &#8216;idle&#8217;, function() { getSpills();} );
              
}

function getSpills() {
                  
var mapCorners = map.getBounds();
                  
var ne = mapCorners.getNorthEast(); // LatLng of the north-east corner
                  
var sw = mapCorners.getSouthWest(); // LatLng of the south-west corder

sqlParameters.latMin = sw.lat();
                  
sqlParameters.latMax = ne.lat();
                  
sqlParameters.lngMin = sw.lng();
                  
sqlParameters.lngMax = ne.lng();

var newSpillLocations; 

//Get the spill location data
                  
$.ajax({
                      
url : "getSpillLocations.php",
                      
type: "POST",
                      
data : sqlParameters,
                      
dataType : "json",
                      
success: function(data){
                          
SpillLocations = data;
                          
plotSpills(SpillLocations);
                      
},
                      
error: function (data)
                      
{
                          
$( "#no-data" ).dialog( "open" );
                      
}
                  
});
              
}

function plotSpills(spillLocations){
                  
map.clearMarkers(markers);
                  
markers = [];
                  
alreadyMapped = []; //An array to keep track of already populated ATS legal subdivisions
                  
markers.push(selectedMarker);
                  
alreadyMapped.push(selectedMarker.ATSLocation);
                  
//Stick those markers into the map canvas
                  
for (var i = 0; i < spillLocations.length; i++) {
                      
//Dont duplicate the selected marker or LSDs with a marker already.
                      
if (jQuery.inArray(spillLocations[i].Location, alreadyMapped) == -1) {
                    	  
alreadyMapped.push(spillLocations[i].ATSLocation);

var marker = new google.maps.Marker({
                              
position: new google.maps.LatLng(spillLocations[i].Latitude, spillLocations[i].Longitude),
                              
icon: &#8216;spotlight-poi.png&#8217;,
                              
map: map,
                              
ATSLocation: spillLocations[i].Location
                          
});

makeLoadSpillInfoEvent(marker);

markers.push(marker);
                      
}
                  
}
              
}

//The info window function from http://jsfiddle.net/yV6xv/161/
              
function makeLoadSpillInfoEvent(marker) {
                  
google.maps.event.addListener(marker, &#8216;click&#8217;, function() {
                      
//Set the old marker back to red
                      
selectedMarker.setIcon(&#8216;spotlight-poi.png&#8217;);
                      
//Set the new marker to orange
                      
selectedMarker = marker;
                      
selectedMarker.setIcon(&#8216;spotlight-poi-orange.png&#8217;);
                      
loadSpillInfo(marker.ATSLocation);
                  
});
              
}

//A function that fetches the specific spill info and loads it into the spill-info div
              
function loadSpillInfo(ATSLocation) {

var spillInfo = {};

$.ajax({
                      
async: false,
                      
url : "getSpillInfo.php",
                      
type: "POST",
                      
data: $.extend({Location: ATSLocation}, sqlParameters), //send ATS location + filter parameters
                      
dataType : "json",
                      
success: function(data){
                          
spillInfo = data;
                      
},
                      
error: function (data)
                      
{
                          
$( "#no-data" ).dialog( "open" );
                      
}
                  
});

//Clear existing content
                  
document.getElementById("spill-info").innerHTML = "";

//A count of the selected incidents for the user to know how many spill info tables have been loaded
                  
var incidentCount = document.createElement(&#8216;strong&#8217;);
                  
incidentCount.innerHTML = &#8216;Number of incidents selected: &#8216;+spillInfo.length.toString()+'<br>&#8217;;
                  
document.getElementById("spill-info").appendChild(incidentCount);

//Iterate through the JSON encoded spill info objects and create a table for each
                  
for (var i = 0; i < spillInfo.length; i++){
                	  
var lineBreak = document.createElement(&#8216;br&#8217;);
	                  
var table = document.createElement(&#8216;table&#8217;);

//Populated the new table element
	                  
for (var key in spillInfo[i]) {
	                      
if (spillInfo[i].hasOwnProperty(key)) {
	                          
var row = document.createElement(&#8216;tr&#8217;);
	                          
row.style.backgroundColor = "#ffebb8";
	                          
var cell1 = row.insertCell(0);
	                          
cell1.innerHTML = &#8216;<strong>&#8217;+key+'</strong>&#8217;;
	                          
var cell2 = row.insertCell(1);
	                          
cell2.innerHTML = spillInfo\[i\]\[key\];
	                          
table.appendChild(row);
	                      
}
	                  
}

//Put the table into the div
	                  
document.getElementById("spill-info").appendChild(lineBreak);
	                  
document.getElementById("spill-info").appendChild(table);
	          
}
	          
//Open the spill info accordion section
	          
$(&#8216;#accordion&#8217;).accordion("option", "active", 1);
	      
}

//A customized clearOverlays function to remove the defunct markers but keep the selected one.
              
google.maps.Map.prototype.clearMarkers = function() {
                  
for (var i = 0; i < markers.length; i++ ) {
                      
//Dont kill the selected marker, we want it to persist
                      
if (!(markers[i] === selectedMarker)) {
                          
markers[i].setMap(null);
                      
}
                  
}
              
}
          
</script>
      
</head>
      
<body>
          
<div id="map-canvas" style="width:100%;height:100%;"></div>
          
<div id="info-panel" style="text-align:left;">
              
<div class="text-block">
                  
<h3>Alberta Oil and Gas Incidents 1975 &#8211; 2013</h3>
                  
This is a map that interactively graphs all of the Oil and Gas related spills in alberta between the years 1975 and 2013. It is based on the data acquired by <a href="http://globalnews.ca/news/622513/open-data-alberta-oil-spills-1975-2013/" target="blank">Global News</a> from the <a href="http://en.wikipedia.org/wiki/Energy\_Resources\_Conservation_Board" target="blank">ERCB</a> (now the <a href="http://www.aer.ca/" target="blank">AER</a>).
                  
</br>
                  
</br>
                  
For optimal loading speeds and a clean map, it caps the number of incidents displayed to the 100 biggest spills (by volume in m<sup>3</sup>) in the current map area. Try zooming in to see more spills, or play with the provided filters to see more incidents.
                  
</br>
                  
<p>
                      
Learn more about this project at:
                      
<a href="http://everettsprojects.com/2014/06/24/mapping-oil-and-gas-incidents-in-alberta-improvements/" target="blank">everettsprojects.com</a>
                  
</p>
              
</div>
              
<div id="accordion">
                  
<h3>Filter the Results</h3>
                  
<div id="filter-pane">
                      
<p>
                          
<label for="amount">Years:</label>
                          
<span style="float:right;">
                              
<input type="text" class="amount1" id="years\_amount\_low" size="4">
                              
<span class="orange-text"> &#8211; </span>
                              
<input type="text" class="amount2" id="years\_amount\_high" size="4">
                          
</span>
                      
</p>

<div class="slider" id="years" data-begin="1975" data-end="2013" data-step="1"> </div>

<p>
                          
<label for="amount">Volume:</label>
                          
<span style="float:right;">
                              
<input type="text" class="amount1" id="volume\_amount\_low" size="9">
                              
<span class="orange-text"> &#8211; </span>
                              
<input type="text" class="amount2" id="volume\_amount\_high" size="9">
                              
<span class="orange-text"> m<sup>3</sup></span>
                          
</span>
                      
</p>

<div class="slider" id="volume" data-begin="0" data-end="37000000" data-step="1000"> </div>
                      
<br>
                      
<p>
                          
<div class="ui-widget">
                              
<label for="licensee-selector">Company: </label>
                              
<input id="licensee-selector" style="width:17em;" class="orange-text"> <span style="float:right;">[<a href=# id="licensee-clear">X</a>]</span>
                              
<br>
                          
</div>
                      
</p>

<p>
                          
<ul id="substance-menu">
                              
<li><a href="#">Substance: <span id="substance-selected" class="orange-text">All</span></a>
                                  
<ul id="substance-links">

</ul>
                              
</li>
                          
</ul>
                      
</p>
                      
<p>
                          
<ul id="source-menu">
                              
<li><a href="#">Source: <span id="source-selected" class="orange-text">All</span></a>
                                  
<ul id="source-links">

</ul>
                              
</li>
                          
</ul>
                      
</p>
                  
</div>
                  
<h3>Incident Details</h3>
                  
<div id="spill-info">
                      
This is where the data for a selected spill will be displayed. Click one to check it out!
                  
</div>
              
</div>
              
<div class="text-block">
                  
<p>
                      
<a href="#" id="disclaimer-opener">Disclaimer</a> &#8211;
                      
<a href="#" id="license-opener">Copyright (c) 2014 Everett Robinson</a> &#8211;
		      
<a href="http://everettsprojects.com/2014/06/24/mapping-oil-and-gas-incidents-in-alberta-improvements/">ver. 2</a>
                  
</p>
              
</div>
          
</div>
          
<div id="disclaimer" title="Disclaimer:" style="font-size:0.75em;">
              
<p>
                  
I do not under any circumstances guarantee the accuracy or truthfulness of the provided information. Furthermore, this project should not be taken as representative of the former ERCB, AER, or any other applicable parties.
                  
<br>
                  
<br>
                  
Due to the use of the Alberta Township System, many locations are approximations only. In general, points can be considered accurate to 200 metres.
                  
<br>
                  
<br>
                  
Any spills originating from trans-provincial or trans-national pipelines are not included, since they do not fall under the jursdiction of the AER. Furthermore, many spills under 2 m<sup>3</sup> that did not originate from a pipeline may be absent, as they are not required to be reported.
              
</p>
          
</div>
          
<div id="license" title="MIT License:" style="font-size:0.75em;">
              
<p>
                  
Copyright (c) 2014 Everett Robinson
              
</p>
              
<p>
  
This content is released under the MIT License.
  
<br><br>
  
Permission is hereby granted, free of charge, to any person obtaining a copy
  
of this software and associated documentation files (the "Software"), to deal
  
in the Software without restriction, including without limitation the rights
  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  
copies of the Software, and to permit persons to whom the Software is
  
furnished to do so, subject to the following conditions:
  
<br><br>
  
The above copyright notice and this permission notice shall be included in
  
all copies or substantial portions of the Software.
  
<br><br>
  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  
THE SOFTWARE.

</p>
          
</div>
          
<div id="no-data" class="noTitleDialog" style="font-size:0.75em;">
              
<p>
                  
Oops, the spill locations or data couldn&#8217;t be loaded right now.
              
</p>
          
</div>
      
</body>
  
</html>
  
[/code]

My map still lacks one neat feature of the Global News map; the ability to see the cumulative spill volume for a particular legal subdivision. Since my map does not narrow the substances down to crude oil and its related products, it&#8217;s a non-trivial problem to effectively add up the cumulative volumes released without without blindly adding different substances together. Of course, blindly adding these values together will produce confusing and potentially meaningless results. In light of these concerns, cumulative volumes for each LSD is a feature I don&#8217;t care to reproduce at the time being.

With all of these changes, I&#8217;ve convinced myself that the project is done for the time being. Of course I know this isn&#8217;t true, and that there will always be bigger, better, faster, and less buggy versions to work towards. So until then, I hope you enjoy this improved version of the web application.