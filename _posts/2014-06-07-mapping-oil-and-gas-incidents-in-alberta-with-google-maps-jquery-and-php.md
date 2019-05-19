---
id: 930
title: Mapping Oil and Gas Incidents in Alberta with Google Maps, JQuery, and PHP
date: 2014-06-07T00:00:24+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=930
permalink: /2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/
geo_public:
  - "0"
image: /wp-content/uploads/2014/06/spills-672x372.png
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
comments: true
---
### [<img class="aligncenter wp-image-989 size-full" src="/wp-content/uploads/2014/06/spills.png" alt="spills" width="594" height="324" srcset="/wp-content/uploads/2014/06/spills.png 1440w, /wp-content/uploads/2014/06/spills-300x163.png 300w, /wp-content/uploads/2014/06/spills-1024x558.png 1024w" sizes="(max-width: 594px) 100vw, 594px" />](/spills/#)

[**_There is an updated version of this project with a number of improvements._**](/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/)

### Sections:

  1. [Motivations](#motivation)
  2. [The Database](#database)
  3. [The Code](#code)
  4. [Considerations and Caveats](#considerations)

<div id="motivation"></div>
### Motivation:

This is a project I conceived of back in university as an environmental science student, but never could make because the spill data on which it relies was not freely available. Later, while I was preoccupied with travel, Global News, a Canadian News broadcaster managed to get a copy of the database using a freedom of information request. They released  a <a href="http://globalnews.ca/news/571494/introduction-37-years-of-oil-spills-in-alberta/">news story including an interactive map of their own</a>, which does some cool things this one does not. It plots the spills in such a way that the marker size reflects the cumulative volume spilled at that location, and it even breaks this cumulative spill up into multiple incidents by date if applicable. On the other hand, it only displays spills for Crude Oil and a few other related substances, offers a very limited view-port that cannot show the entire province, and does not provide any real filtering capabilities. Thankfully, Global News released <a href="http://globalnews.ca/news/622513/open-data-alberta-oil-spills-1975-2013/">their copy of the database</a>, so I can build my own map that includes some of the features I think are cool (even if I&#8217;m a year late to the party). The database is in a .csv format, which I have since converted back to a SQL (mySQL) database. Unfortunately this back and forth conversion poses certain problems like truncated values in certain fields. Luckily these issues are fairly minimal.


So without further delay, lets move on to the process of converting the database back to SQL:


<div id="database"></div>
### The Database:

I am assuming you have created a database already and have a database user that can access it. Making this user read only will also not be such a bad idea, since the web application will never need to modify values. All of this can be easily accomplished with phpMyAdmin, or a similar tool.

First lets create the table structure:

{% highlight sql %}
CREATE TABLE `Spills` (
  `IncidentNumber` int DEFAULT NULL,
  `IncidentType` varchar(255) DEFAULT NULL,
  `Latitude` decimal(10,8) DEFAULT NULL,
  `Longitude` decimal(11,8) DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `IncidentLSD` int DEFAULT NULL,
  `IncidentSection` int DEFAULT NULL,
  `IncidentTownship` int DEFAULT NULL,
  `IncidentRange` int DEFAULT NULL,
  `IncidentMeridian` int DEFAULT NULL,
  `LicenceNumber` varchar(255) DEFAULT NULL,
  `LicenceType` varchar(255) DEFAULT NULL,
  `IncidentDate` varchar(255) DEFAULT NULL,
  `IncidentNotificationDate` varchar(255) DEFAULT NULL,
  `IncidentCompleteDate` varchar(255) DEFAULT NULL,
  `Source` varchar(255) DEFAULT NULL,
  `CauseCategory` varchar(255) DEFAULT NULL,
  `CauseType` varchar(255) DEFAULT NULL,
  `FailureType` varchar(255) DEFAULT NULL,
  `StrikeArea` varchar(255) DEFAULT NULL,
  `FieldCentre` varchar(255) DEFAULT NULL,
  `LicenseeID` int(4) DEFAULT NULL,
  `LicenseeName` varchar(255) DEFAULT NULL,
  `InjuryCount` int DEFAULT NULL,
  `FatalityCount` int DEFAULT NULL,
  `Jurisdiction` varchar(255) DEFAULT NULL,
  `ReleaseOffsite` varchar(255) DEFAULT NULL,
  `SensitiveArea` varchar(255) DEFAULT NULL,
  `PublicAffected` varchar(255) DEFAULT NULL,
  `EnvironmentAffected` varchar(255) DEFAULT NULL,
  `WildlifeLivestockAffected` varchar(255) DEFAULT NULL,
  `AreaAffected` varchar(255) DEFAULT NULL,
  `PublicEvacuatedCount` int DEFAULT NULL,
  `ReleaseCleanupDate` varchar(255) DEFAULT NULL,
  `PipelineLicenceSegmentID` int DEFAULT NULL,
  `PipelineLicenceLineNo` int DEFAULT NULL,
  `PipeDamageType` varchar(255) DEFAULT NULL,
  `PipeTestFailure` varchar(255) DEFAULT NULL,
  `PipelineOutsideDiameter(mm)` float DEFAULT NULL,
  `PipeGrade` varchar(255) DEFAULT NULL,
  `PipeWallThickness(mm)` float DEFAULT NULL,
  `Substance Released` varchar(255) DEFAULT NULL,
  `Volume Released` float DEFAULT NULL,
  `Volume Recovered` float DEFAULT NULL,
  `Volume Units` varchar(255) DEFAULT NULL,
  `Substance Released 2` varchar(255) DEFAULT NULL,
  `Volume Released 2` float DEFAULT NULL,
  `Volume Recovered 2` float DEFAULT NULL,
  `Volume Units 2` varchar(255) DEFAULT NULL,
  `Substance Released 3` varchar(255) DEFAULT NULL,
  `Volume Released 3` float DEFAULT NULL,
  `Volume Recovered 3` float DEFAULT NULL,
  `Volume Units 3` varchar(255) DEFAULT NULL,
  `Substance Released 4` varchar(255) DEFAULT NULL,
  `Volume Released 4` float DEFAULT NULL,
  `Volume Recovered 4` float DEFAULT NULL,
  `Volume Units 4` varchar(255) DEFAULT NULL,
   UNIQUE KEY `IncidentNumber` (`IncidentNumber`),
   KEY `IncidentNumber_2` (`IncidentNumber`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8
{% endhighlight %}

With the table made, we will load the Global News .CSV file into the table. Be sure to point it to the right file location for your server:

{% highlight sql %}
LOAD DATA LOCAL INFILE '<PATH TO THE FILE>/OPENDATA_spills.csv' INTO TABLE Spills
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
{% endhighlight %}

Now we want to reformat all of the date fields so that they can be real dates within the database:

{% highlight sql %}
UPDATE Spills
SET IncidentDate = DATE(STR_TO_DATE(IncidentDate, '%m/%d/%Y'))
WHERE DATE(STR_TO_DATE(IncidentDate, '%m/%d/%Y')) <> '0000-00-00';

ALTER TABLE `Spills` CHANGE `IncidentDate` `IncidentDate` DATE NULL DEFAULT NULL;

UPDATE Spills
SET IncidentNotificationDate = DATE(STR_TO_DATE(IncidentNotificationDate, '%m/%d/%Y'))
WHERE DATE(STR_TO_DATE(IncidentNotificationDate, '%m/%d/%Y')) <> '0000-00-00';

ALTER TABLE `Spills` CHANGE `IncidentNotificationDate` `IncidentNotificationDate` DATE NULL DEFAULT NULL;

UPDATE Spills
SET IncidentCompleteDate = DATE(STR_TO_DATE(IncidentCompleteDate, '%m/%d/%Y'))
WHERE DATE(STR_TO_DATE(IncidentCompleteDate, '%m/%d/%Y')) <> '0000-00-00';

ALTER TABLE `Spills` CHANGE `IncidentCompleteDate` `IncidentCompleteDate` DATE NULL DEFAULT NULL;

UPDATE Spills
SET ReleaseCleanupDate = DATE(STR_TO_DATE(ReleaseCleanupDate, '%m/%d/%Y'))
WHERE DATE(STR_TO_DATE(ReleaseCleanupDate, '%m/%d/%Y')) <> '0000-00-00';

ALTER TABLE `Spills` CHANGE `ReleaseCleanupDate` `ReleaseCleanupDate` DATE NULL DEFAULT NULL;
{% endhighlight %}

There is also an issue with inconsistent units. Some entries have units of &#8220;m3&#8221;, and others are in units of &#8220;103m3&#8221;. Now it&#8217;s obviously not the case that the units are multiples of 103 in m<sup>3</sup>, but rather in 10<sup>3</sup> m<sup>3</sup>. In order for the volume filter to be implemented correctly, we&#8217;ll want consistent units:

{% highlight sql %}
UPDATE Spills SET  `Volume Released` = `Volume Released`*1000 WHERE `Volume Units`="103m3";
UPDATE Spills SET  `Volume Recovered` = `Volume Recovered`*1000 WHERE `Volume Units`="103m3";

UPDATE Spills SET `Volume Released 2` = `Volume Released 2`*1000 WHERE `Volume Units 2`="103m3";
UPDATE Spills SET `Volume Recovered 2` = `Volume Recovered 2`*1000 WHERE `Volume Units 2`="103m3";

UPDATE Spills SET `Volume Released 3` = `Volume Released 3`*1000 WHERE `Volume Units 3`="103m3";
UPDATE Spills SET `Volume Recovered 3` = `Volume Recovered 3`*1000 WHERE `Volume Units 3`="103m3";

UPDATE Spills SET `Volume Released 4` = `Volume Released 4`*1000 WHERE `Volume Units 4`="103m3";
UPDATE Spills SET `Volume Recovered 4` = `Volume Recovered 4`*1000 WHERE `Volume Units 4`="103m3";
{% endhighlight %}

That takes care of differing units, so now we don&#8217;t really need those units columns, since everything is in m<sup>3</sup> now.

{% highlight sql %}
ALTER TABLE `Spills`
DROP `Volume Units`,
DROP `Volume Units 2`,
DROP `Volume Units 3`,
DROP `Volume Units 4`;
{% endhighlight %}

As this table isn&#8217;t going to be updated often (if at all), we&#8217;ll want to index anything that will be used as a search parameter.

{% highlight sql %}
ALTER TABLE `Spills` ADD INDEX( `Latitude`, `Longitude`, `IncidentDate`, `LicenseeName`, `Source`, `Substance Released`, `Volume Released`);
{% endhighlight %}

And there we have it, a database that should be ready for the web application that will sit on top of it.

<div id="code"></div>
### The Code:
<a href="/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/"><em>There is an updated version of this project with a number of improvements.</em></a>

If you just want a copy of all the files necessary (for version 1), then I have them <a href="/spillsv1/spills.zip">all in a zipped archive</a>. Don&#8217;t forget to go in and change the values of config.inc.php to reflect your own MySQL database.

For everyone else, lets take a closer look at the code that makes it all work, starting with the JavaScript laden index.html file:

<div id="index"></div>
#### index.html

{% highlight html %}
  <!DOCTYPE html>
  <html>
      <head>
          <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
          <meta charset="utf-8">
          <title>Alberta Oil and Gas Incidents 1975 - 2013</title>
          <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
          <link href="/spills/default.css" rel="stylesheet">
          <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
          <script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
          <script type="text/javascript"
              src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCIxpXOSPJWNG7TnhMYq-Q2hPcM7zEQs8g&sensor=false">
          </script>
          <script>
              //Make a bunch of variables to track the filters and map boundaries
              var sqlParameters = {
                  currentSubstance : 'All',
                  currentSource : 'All',
                  currentLicensee: 'All',
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
                      dialogClass: 'noTitleDialog',
                      open: function(event, ui){
                          setTimeout("$('#no-data').dialog('close')",3000);
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
                              var sliderlow = ("#" + $(this).attr("id") + "_amount_low");
                              $(sliderlow).val(ui.values[0]);

                              var sliderhigh = ("#" + $(this).attr("id") + "_amount_high");
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
                      var sliderlow = ("#" + $(this).attr("id") + "_amount_low");
                      $(sliderlow).val($(this).slider("values", 0));

                      var sliderhigh = ("#" + $(this).attr("id") + "_amount_high");
                      $(sliderhigh).val($(this).slider("values", 1));
                  })

                  //When the text box is changed, update the slider
                  $('.amount1').change(function () {
                      var value = this.value,
                      selector = $("#" + this.id.split('_')[0]);
                      selector.slider("values", 0, value);
                  })
                  $('.amount2').change(function () {
                      var value = this.value,
                      selector = $("#" + this.id.split('_')[0]);
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
                      alert("Couldn't retrieve the licensee list. A page refresh will usually fix this.");
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
                      sqlParameters.currentLicensee = 'All';
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
                          alert("Couldn't retrieve the substance list. A page refresh will usually fix this.");
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
                          alert("Couldn't retrieve the source list. A page refresh will usually fix this.");
                      }
                  });

                  //Build the lists using the database results
                  //Function courtesy of http://stackoverflow.com/questions/11128700/create-a-ul-and-fill-it-based-on-a-passed-array
                  function constructLI(domID, array) {

                      var fieldID = (domID.split("-"))[0]+"-selected";

                      for(var i = 0; i < array.length; i++) {
                          // Create the list item:
                          var member = document.createElement('li');

                          // Set its contents:
                          var linkText = document.createTextNode(array[i]);
                          var link = document.createElement('a');
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
                                  icon: 'spotlight-poi.png',
                                  map: map,
                                  spillID: null
                          });
              var spillLocations;

              //Initialize when the map is done
              google.maps.event.addDomListener(window, 'load', initialize);

              function initialize() {         clearStyle: true;
                  var middleEarth = new google.maps.LatLng(54.5, -115.0);
                  var mapOptions = {
                      zoom: 6,
                      center: middleEarth,
                      mapTypeId: google.maps.MapTypeId.ROADMAP
                  };

                  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);       

                  makeGetSpillsEvent();
              }

              function makeGetSpillsEvent(){
                  google.maps.event.addListener(map, 'idle', function() { getSpills();} );
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
                  markers.push(selectedMarker);
                  //Stick those markers into the map canvas
                  for (var i = 0; i < spillLocations.length; i++) {
                      //Dont duplicate the selected marker.
                      if (selectedMarker.spillID !==  spillLocations[i].IncidentNumber) {
                          var marker = new google.maps.Marker({
                              position: new google.maps.LatLng(spillLocations[i].Latitude, spillLocations[i].Longitude),
                              icon: 'spotlight-poi.png',
                              map: map,
                              spillID: spillLocations[i].IncidentNumber
                          });
                      }

                      makeLoadSpillInfoEvent(marker);

                      markers.push(marker);
                  }
              }

              //The info window function from http://jsfiddle.net/yV6xv/161/
              function makeLoadSpillInfoEvent(marker) {
                  google.maps.event.addListener(marker, 'click', function() {
                      //Set the old marker back to red
                      selectedMarker.setIcon('spotlight-poi.png');
                      //Set the new marker to orange
                      selectedMarker = marker;
                      selectedMarker.setIcon('spotlight-poi-orange.png');
                      loadSpillInfo(marker.spillID);
                  });
              }

              //A function that fetches the specific spill info and loads it into the spill-info div
              function loadSpillInfo(spillID) {

                  var spillInfo = {}

                  $.ajax({
                      async: false,
                      url : "getSpillInfo.php",
                      type: "POST",
                      data: {'incidentnumber':spillID},
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
                  var table = document.createElement('table');

                  //Populated the new table element
                  for (var key in spillInfo) {
                      if (spillInfo.hasOwnProperty(key)) {
                          var row = document.createElement('tr');
                          row.style.backgroundColor = "#ffebb8";
                          var cell1 = row.insertCell(0);
                          cell1.innerHTML = '<strong>'+key+'</strong>';
                          var cell2 = row.insertCell(1);
                          cell2.innerHTML = spillInfo[key];
                          table.appendChild(row);
                      }
                  }

                  //Put the table into the div and open the spill info accordion section
                  document.getElementById("spill-info").appendChild(table);
                  $('#accordion').accordion("option", "active", 1);
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
                  <h3>Alberta Oil and Gas Incidents 1975 - 2013</h3>
                  This is a map that interactively graphs all of the Oil and Gas related spills in alberta between the years 1975 and 2013. It is based on the data acquired by <a href="http://globalnews.ca/news/622513/open-data-alberta-oil-spills-1975-2013/" target="blank">Global News</a> from the <a href="http://en.wikipedia.org/wiki/Energy_Resources_Conservation_Board" target="blank">ERCB</a> (now the <a href="http://www.aer.ca/" target="blank">AER</a>).
                  </br>
                  </br>
                  For optimal loading speeds and a clean map, it caps the number of incidents displayed to the 100 biggest spills (by volume in m<sup>3</sup>) in the current map area. Try zooming in to see more spills, or play with the provided filters to see more incidents.
                  </br>
                  <p>
                      Learn more about this project at:
                      <a href="/2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/" target="blank">everettsprojects.com</a>
                  </p>
              </div>
              <div id="accordion">
                  <h3>Filter the Results</h3>
                  <div id="filter-pane">
                      <p>
                          <label for="amount">Years:</label>
                          <span style="float:right;">
                              <input type="text" class="amount1" id="years_amount_low"  size="4">
                              <span class="orange-text"> - </span>
                              <input type="text" class="amount2" id="years_amount_high" size="4">
                          </span>
                      </p>

                      <div class="slider" id="years" data-begin="1975" data-end="2013" data-step="1"> </div>

                      <p>
                          <label for="amount">Volume:</label>
                          <span style="float:right;">
                              <input type="text" class="amount1" id="volume_amount_low" size="9">
                              <span class="orange-text"> - </span>
                              <input type="text" class="amount2" id="volume_amount_high" size="9">
                              <span class="orange-text"> m<sup>3</sup></span>
                          </span>
                      </p>

                      <div class="slider" id="volume" data-begin="0" data-end="37000000" data-step="1000"> </div>
                      <br>
                      <p>
                          <div class="ui-widget">
                              <label for="licensee-selector">Company: </label>
                              <input id="licensee-selector" size="29" class="orange-text">  <span style="float:right;">[<a href=# id="licensee-clear">X</a>]</span>
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
                      <a href="#" id="disclaimer-opener">Disclaimer</a> -
                      <a href="#" id="license-opener">Copyright (c) 2014 Everett Robinson</a>
                  </p>
              </div>
          </div>
          <div id="disclaimer" title="Disclaimer:" style="font-size:75%;">
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
          <div id="license" title="MIT License:" style="font-size:75%;">
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
          <div id="no-data" class="noTitleDialog" style="font-size:75%;">
              <p>
                  Oops, the spill locations or data couldn't be loaded right now.
              </p>
          </div>
      </body>
  </html>
{% endhighlight %}

So that&#8217;s a bit of a long file, but I&#8217;ve tried to describe each function&#8217;s purpose, and have laid out the JavaScript as best as possible to provide a rational flow. Overall, the JavaScript is broken into 4 parts:

<ol>
  <li>
    <span style="font-family:Consolas, Monaco, monospace;font-size:12px;line-height:18px;">The JQuery UI widgets that implement the filters and update the map points when changed</span>
  </li>
  <li>
    <span style="font-family:Consolas, Monaco, monospace;font-size:12px;line-height:18px;">The google maps code that displays the map and update the points when the view-port is moved</span>
  </li>
  <li>
    <span style="font-family:Consolas, Monaco, monospace;font-size:12px;line-height:18px;">The JQuery/AJAX code that fetches the map points using the view-port and filter values</span>
  </li>
  <li>
    <span style="font-family:Consolas, Monaco, monospace;font-size:12px;line-height:18px;">The JQuery/AJAX code that gets all of the info for a spill if it is selected</span>
  </li>
</ol>

There is then the HTML necessary for rendering the webpage, which relies on the following CSS file (default.css):

<div id="css"></div>
#### default.css

{% highlight css %}
html, body {
  background-color:#b0c4de;
  height: 100%;
  margin: 0;
  padding: 0;
  font-size: 100%;
}

#map-canvas, #map_canvas {
  height: 100%;
}

@media print {
  html, body {
    height: auto;
  }

  #map-canvas, #map_canvas {
    height: 650px;
  }
}

#info-panel {
  width: 25%;
  max-height: 96%;
  position: absolute;
  font-size: 75%;
  top: 10px;
  left: 90px;
  background-color: #fff;
  padding: 2px;
  border: 1px solid #999;
  background: rgba(255, 255, 255, 1);
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  -ms-border-radius: 5px;
  -o-border-radius: 5px;
  border-radius: 5px;
  border: outset 1px #a1b5cf;
}

.text-block {
  margin: 10px;
  border-width: 2px;
  text-align: center;
}

#accordion {
  margin: 10px;
  border-width: 2px;
  overflow: auto;
}

#filter-pane {
  overflow: auto;
  font-size: smaller;
}

.amount1, .amount2 {
  border: 0;
  color: #f6931f;
  font-weight: bold;
  text-align: center;
}

ul.ui-autocomplete {
  overflow: auto;
  width: 200px;
  max-height: 200px;
  font-size: 75%;

}

#substance-links {
  overflow: auto;
  width: 200px;
  max-height: 200px;
  z-index: 1;
}

#source-links {
  overflow: auto;
  width: 200px;
  max-height: 200px;
  z-index: 1;
}

.orange-text {
  color: #f6931f;
  font-weight:bold;
}

#spill-info {
  overflow: auto;
  font-size:smaller;
  max-height: 400px;
}

.noTitleDialog {
  text-align: center;
}

.noTitleDialog .ui-dialog-titlebar {
  display:none;
}

.ui-autocomplete-loading {
    background: white url('images/ui-anim_basic_16x16.gif') right center no-repeat;
}
{% endhighlight %}

And Finally, six PHP files necessary for interfacing our web page to the database:

<div id="getSpillLocations"></div>
#### getSpillLocations.php

{% highlight php %}
<?php
require('config.inc.php');

//Get all of the POST data
$currentlicensee = $_POST['currentLicensee'];
$currentsubstance = $_POST['currentSubstance'];
$currentsource = $_POST['currentSource'];
$yearmin = $_POST['yearMin'];
$yearmax = $_POST['yearMax'];
$volumemin = $_POST['volumeMin'];
$volumemax = $_POST['volumeMax'];
$latmin = $_POST['latMin'];
$latmax = $_POST['latMax'];
$longmin = $_POST['lngMin'];
$longmax = $_POST['lngMax'];

// Fix the years to go from start of first year to end of the last.
$datemin = $yearmin."-01-01";
$datemax = $yearmax."-12-31";

//By using PDO and prepare, everything is automagically escaped
$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);

//Start building the statement with the base of the query
$stmtString = "SELECT `IncidentNumber`, `Latitude`, `Longitude` FROM `Spills` WHERE (((`Longitude` BETWEEN :longMin AND :longMax) AND (`Latitude` BETWEEN :latMin AND :latMax) AND (`IncidentDate` BETWEEN :dateMin AND :dateMax) AND (`Volume Released` BETWEEN :volumeMin AND :volumeMax))";

//Add in the filters if they're set
if ($currentlicensee !== "All") {
    $stmtString .= " AND `LicenseeName` = :licensee";
}
if ($currentsubstance !== "All") {
    $stmtString .= " AND `Substance Released` = :substance";
}
if ($currentsource !== "All") {
    $stmtString .= " AND `Source` = :source";
}

//Finish the statement with the sorting and limit parts
$stmtString .= ") ORDER BY `Volume Released` DESC LIMIT 100";

//Bind all of the parameters
$stmt = $db->prepare($stmtString);
if (strpos($stmtString,':licensee') !== false) {
    $stmt->bindValue(':licensee', strval($currentlicensee), PDO::PARAM_STR);
}
if (strpos($stmtString,':source') !== false) {
    $stmt->bindValue(':source', strval($currentsource), PDO::PARAM_STR);
}
if (strpos($stmtString,':substance') !== false) {
    $stmt->bindValue(':substance', strval($currentsubstance), PDO::PARAM_STR);
}
$stmt->bindValue(':latMin', strval($latmin), PDO::PARAM_STR);
$stmt->bindValue(':latMax', strval($latmax), PDO::PARAM_STR);
$stmt->bindValue(':longMin', strval($longmin), PDO::PARAM_STR);
$stmt->bindValue(':longMax', strval($longmax), PDO::PARAM_STR);
$stmt->bindValue(':dateMin', strval($datemin), PDO::PARAM_STR);
$stmt->bindValue(':dateMax', strval($datemax), PDO::PARAM_STR);
$stmt->bindValue(':volumeMin', strval($volumemin), PDO::PARAM_STR);
$stmt->bindValue(':volumeMax', strval($volumemax), PDO::PARAM_STR);
$stmt->execute();

//Get the results of the query
$result;
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
//Spit out the results in json form
echo header('Content-type: application/json');
echo json_encode($result);
?>
{% endhighlight %}

<div id="getSpillInfo"></div>
#### getSpillInfo.php

{% highlight php %}
<?php

$incidentNumber = $_POST['incidentnumber'];

require('config.inc.php');
$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);
//By using PDO and prepare, everything is automagically escaped
$stmt = $db->prepare("SELECT * FROM `Spills` WHERE `IncidentNumber` = :incidentNumber");
$stmt->bindValue(':incidentNumber', strval($incidentNumber), PDO::PARAM_STR);
/*** execute the prepared statement ***/
$stmt->execute();
$result = $stmt->fetch(PDO::FETCH_ASSOC);

echo header('Content-type: application/json');
echo json_encode($result);

?>
{% endhighlight %}

<div id="getLicensees"></div>
#### getLicensees.php
{% highlight php %}
<?php
require('config.inc.php');

$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);
//By using PDO and prepare, everything is automagically escaped
$stmt = $db->prepare("SELECT `LicenseeName` FROM `Spills` GROUP BY `LicenseeName` ORDER BY `Spills`.`LicenseeName` ASC LIMIT 2000");
$stmt->execute();
$result = $stmt->fetchAll(PDO::FETCH_COLUMN, 0);

echo header('Content-type: application/json');
echo json_encode($result);

?>
{% endhighlight %}

<div id="getSubstances"></div>
#### getSubstances.php
{% highlight php %}
<?php
require('config.inc.php');

$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);
//By using PDO and prepare, everything is automagically escaped
$stmt = $db->prepare("SELECT `Substance Released` FROM `Spills` GROUP BY `Substance Released` ORDER BY `Spills`.`Substance Released` ASC LIMIT 100");
$stmt->execute();
$result = $stmt->fetchAll(PDO::FETCH_NUM);

echo header('Content-type: application/json');
echo json_encode($result);

?>
{% endhighlight %}

<div id="getSources"></div>
#### getSources.php
{% highlight php %}
<?php
require('config.inc.php');

$db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);
//By using PDO and prepare, everything is automagically escaped, not that it's necessary here
$stmt = $db->prepare("SELECT `Source` FROM `Spills` GROUP BY `Source` ORDER BY `Spills`.`Source` ASC LIMIT 100");
$stmt->execute();
$result = $stmt->fetchAll(PDO::FETCH_NUM);

echo header('Content-type: application/json');
echo json_encode($result);

?>
{% endhighlight %}

<div id="config"></div>
#### config.inc.php
{% highlight php %}
<?php
// These are the login credentials for your MySQL database,
// don't forget to set them.
$dbhost = change me;
$dbname = change me;
$dbuser = change me;
$dbpass = change me;
?>
{% endhighlight %}

The first file, getSpillLocations.php, does what it sounds like. It takes all of the filter parameters along with the map boundaries, and then returns a JSON encoded list of coordinates and spill ID numbers to be plotted. The SQL statement is built based on the parameters passed, and then fulfilled using PHP Data Objects (PDO). The second, getSpillInfo.php, takes a spill ID number, and uses it to return all of the data for that spill as JSON object.<br /> The third, fourth, and fifth scripts are used to fetch lists from the database that are used to populate the menu widgets in the filter panel. They do not require any parameters to be passed, since they just return a list containing all of the existing values for each field. Finally, config.inc.php is simply a file containing the database access credentials, meant to be included in the five other scripts.

<div id="considerations"></div>

### Considerations and Caveats:

The ERCB/AER uses the Alberta Township System (ATS) for reporting locations, which means the latitudes and longitudes in the database are converted values that represent the centre of the smallest unit in the ATS scheme; a Legal Sub-Division (LSD). Since a LSD is 400m along each side, it can be said that any plotted location is accurate to +/- 200m in each axis. This poses another problem however; certain legal subdivisions will have had multiple incidents on them in the 37 year period displayed. A great example is the region near Turner Valley:

<div id="attachment_999" style="width: 600px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2014/06/spills-overlap-animation21.gif"><img class="wp-image-999 size-full" src="/wp-content/uploads/2014/06/spills-overlap-animation21.gif" alt="spills-overlap-animation2" width="590" height="500" /></a>

<p class="wp-caption-text">
  Overlapping spill incidents near Turner Valley need to be differentiated using the provided filters.
</p>

Here, several of the spills in this area were isolated using the provided filters. Unfortunately, there is not currently a mechanism to indicate that overlapping markers exist. The user will either need to have keen eyes to spot the signs, like a slight red border around the yellow selected marker, or play around with the filters to confirm any suspicions.

Another consideration, which is not one I have control over is that any spills originating from trans-provincial or trans-national pipelines are not included, since they do not fall under the jurisdiction of the AER. Furthermore, many spills under 2 m<sup>3</sup> that did not originate from a pipeline may be absent, as they are not required to be reported.

A final issue is that there are in fact 3 members of the database that do not possess a valid latitude or longitude; these fields are 0. The incident numbers are 19940377, 19850326, and 19871009 for reference. This means they are actually plotted in the south Atlantic, off the coast of Africa:

<div id="attachment_1004" style="width: 604px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2014/06/spills-atlantic.png"><img class="size-full wp-image-1004" src="/wp-content/uploads/2014/06/spills-atlantic.png" alt="These incidents are plotted in the wrong location at Latitude: 0, Longitude: 0" width="594" height="324" srcset="/wp-content/uploads/2014/06/spills-atlantic.png 1440w, /wp-content/uploads/2014/06/spills-atlantic-300x163.png 300w, /wp-content/uploads/2014/06/spills-atlantic-1024x559.png 1024w" sizes="(max-width: 594px) 100vw, 594px" /></a>

  <p class="wp-caption-text">
    These incidents are plotted in the wrong location at Latitude: 0, Longitude: 0
  </p>
</div>

Now, I could theoretically go in and correct the values for these three points by converting the ATS coordinates manually, but I decided not to since they illustrate an important point: None of the data in the database is vetted by me. I can not assure that any other data point is valid, though none of the rest are so obviously incorrect.

So with those concerns out of the way; have fun exploring the often hushed side of the oil industry in Alberta.
