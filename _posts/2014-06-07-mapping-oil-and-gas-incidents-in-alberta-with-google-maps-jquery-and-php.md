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
image: https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills-672x372.png
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
### [<img class="aligncenter wp-image-989 size-full" src="http://everett.x10.mx/wp/wp-content/uploads/2014/06/spills.png" alt="spills" width="594" height="324" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills.png 1440w, https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills-300x163.png 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills-1024x558.png 1024w" sizes="(max-width: 594px) 100vw, 594px" />](http://everett.x10.mx/spills/#)

[**_There is an updated version of this project with a number of improvements._**](http://everettsprojects.com/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/)

### Sections:

  1. [Motivations](#motivation)
  2. [The Database](#database)
  3. [The Code](#code)
  4. [Considerations and Caveats](#considerations)

<div id="motivation">
  <h3>
    Motivation:
  </h3>
  
  <p>
    This is a project I conceived of back in university as an environmental science student, but never could make because the spill data on which it relies was not freely available. Later, while I was preoccupied with travel, Global News, a Canadian News broadcaster managed to get a copy of the database using a freedom of information request. They released  a <a href="http://globalnews.ca/news/571494/introduction-37-years-of-oil-spills-in-alberta/">news story including an interactive map of their own</a>, which does some cool things this one does not. It plots the spills in such a way that the marker size reflects the cumulative volume spilled at that location, and it even breaks this cumulative spill up into multiple incidents by date if applicable. On the other hand, it only displays spills for Crude Oil and a few other related substances, offers a very limited view-port that cannot show the entire province, and does not provide any real filtering capabilities. Thankfully, Global News released <a href="http://globalnews.ca/news/622513/open-data-alberta-oil-spills-1975-2013/">their copy of the database</a>, so I can build my own map that includes some of the features I think are cool (even if I&#8217;m a year late to the party). The database is in a .csv format, which I have since converted back to a SQL (mySQL) database. Unfortunately this back and forth conversion poses certain problems like truncated values in certain fields. Luckily these issues are fairly minimal.
  </p>
  
  <p>
    So without further delay, lets move on to the process of converting the database back to SQL:
  </p>
</div>

<div id="database">
  <h3>
    The Database:
  </h3>
  
  <p>
    I am assuming you have created a database already and have a database user that can access it. Making this user read only will also not be such a bad idea, since the web application will never need to modify values. All of this can be easily accomplished with phpMyAdmin, or a similar tool.
  </p>
  
  <p>
    First lets create the table structure:
  </p>
  
  <p>
    [code language=&#8221;sql&#8221;]<br /> CREATE TABLE `Spills` (<br /> `IncidentNumber` int DEFAULT NULL,<br /> `IncidentType` varchar(255) DEFAULT NULL,<br /> `Latitude` decimal(10,8) DEFAULT NULL,<br /> `Longitude` decimal(11,8) DEFAULT NULL,<br /> `Location` varchar(255) DEFAULT NULL,<br /> `IncidentLSD` int DEFAULT NULL,<br /> `IncidentSection` int DEFAULT NULL,<br /> `IncidentTownship` int DEFAULT NULL,<br /> `IncidentRange` int DEFAULT NULL,<br /> `IncidentMeridian` int DEFAULT NULL,<br /> `LicenceNumber` varchar(255) DEFAULT NULL,<br /> `LicenceType` varchar(255) DEFAULT NULL,<br /> `IncidentDate` varchar(255) DEFAULT NULL,<br /> `IncidentNotificationDate` varchar(255) DEFAULT NULL,<br /> `IncidentCompleteDate` varchar(255) DEFAULT NULL,<br /> `Source` varchar(255) DEFAULT NULL,<br /> `CauseCategory` varchar(255) DEFAULT NULL,<br /> `CauseType` varchar(255) DEFAULT NULL,<br /> `FailureType` varchar(255) DEFAULT NULL,<br /> `StrikeArea` varchar(255) DEFAULT NULL,<br /> `FieldCentre` varchar(255) DEFAULT NULL,<br /> `LicenseeID` int(4) DEFAULT NULL,<br /> `LicenseeName` varchar(255) DEFAULT NULL,<br /> `InjuryCount` int DEFAULT NULL,<br /> `FatalityCount` int DEFAULT NULL,<br /> `Jurisdiction` varchar(255) DEFAULT NULL,<br /> `ReleaseOffsite` varchar(255) DEFAULT NULL,<br /> `SensitiveArea` varchar(255) DEFAULT NULL,<br /> `PublicAffected` varchar(255) DEFAULT NULL,<br /> `EnvironmentAffected` varchar(255) DEFAULT NULL,<br /> `WildlifeLivestockAffected` varchar(255) DEFAULT NULL,<br /> `AreaAffected` varchar(255) DEFAULT NULL,<br /> `PublicEvacuatedCount` int DEFAULT NULL,<br /> `ReleaseCleanupDate` varchar(255) DEFAULT NULL,<br /> `PipelineLicenceSegmentID` int DEFAULT NULL,<br /> `PipelineLicenceLineNo` int DEFAULT NULL,<br /> `PipeDamageType` varchar(255) DEFAULT NULL,<br /> `PipeTestFailure` varchar(255) DEFAULT NULL,<br /> `PipelineOutsideDiameter(mm)` float DEFAULT NULL,<br /> `PipeGrade` varchar(255) DEFAULT NULL,<br /> `PipeWallThickness(mm)` float DEFAULT NULL,<br /> `Substance Released` varchar(255) DEFAULT NULL,<br /> `Volume Released` float DEFAULT NULL,<br /> `Volume Recovered` float DEFAULT NULL,<br /> `Volume Units` varchar(255) DEFAULT NULL,<br /> `Substance Released 2` varchar(255) DEFAULT NULL,<br /> `Volume Released 2` float DEFAULT NULL,<br /> `Volume Recovered 2` float DEFAULT NULL,<br /> `Volume Units 2` varchar(255) DEFAULT NULL,<br /> `Substance Released 3` varchar(255) DEFAULT NULL,<br /> `Volume Released 3` float DEFAULT NULL,<br /> `Volume Recovered 3` float DEFAULT NULL,<br /> `Volume Units 3` varchar(255) DEFAULT NULL,<br /> `Substance Released 4` varchar(255) DEFAULT NULL,<br /> `Volume Released 4` float DEFAULT NULL,<br /> `Volume Recovered 4` float DEFAULT NULL,<br /> `Volume Units 4` varchar(255) DEFAULT NULL,<br /> UNIQUE KEY `IncidentNumber` (`IncidentNumber`),<br /> KEY `IncidentNumber_2` (`IncidentNumber`)<br /> ) ENGINE=MyISAM DEFAULT CHARSET=utf8<br /> [/code]
  </p>
  
  <p>
    With the table made, we will load the Global News .CSV file into the table. Be sure to point it to the right file location for your server:
  </p>
  
  <p>
    [code language=&#8221;sql&#8221;]<br /> LOAD DATA LOCAL INFILE &#8216;<PATH TO THE FILE>/OPENDATA_spills.csv&#8217; INTO TABLE Spills<br /> FIELDS TERMINATED BY &#8216;,&#8217;<br /> ENCLOSED BY &#8216;"&#8217;<br /> LINES TERMINATED BY &#8216;\r\n&#8217;<br /> IGNORE 1 LINES<br /> [/code]
  </p>
  
  <p>
    Now we want to reformat all of the date fields so that they can be real dates within the database:
  </p>
  
  <p>
    [code language=&#8221;sql&#8221;]<br /> UPDATE Spills<br /> SET IncidentDate = DATE(STR_TO_DATE(IncidentDate, &#8216;%m/%d/%Y&#8217;))<br /> WHERE DATE(STR_TO_DATE(IncidentDate, &#8216;%m/%d/%Y&#8217;)) <> &#8216;0000-00-00&#8217;;
  </p>
  
  <p>
    ALTER TABLE `Spills` CHANGE `IncidentDate` `IncidentDate` DATE NULL DEFAULT NULL;
  </p>
  
  <p>
    UPDATE Spills<br /> SET IncidentNotificationDate = DATE(STR_TO_DATE(IncidentNotificationDate, &#8216;%m/%d/%Y&#8217;))<br /> WHERE DATE(STR_TO_DATE(IncidentNotificationDate, &#8216;%m/%d/%Y&#8217;)) <> &#8216;0000-00-00&#8217;;
  </p>
  
  <p>
    ALTER TABLE `Spills` CHANGE `IncidentNotificationDate` `IncidentNotificationDate` DATE NULL DEFAULT NULL;
  </p>
  
  <p>
    UPDATE Spills<br /> SET IncidentCompleteDate = DATE(STR_TO_DATE(IncidentCompleteDate, &#8216;%m/%d/%Y&#8217;))<br /> WHERE DATE(STR_TO_DATE(IncidentCompleteDate, &#8216;%m/%d/%Y&#8217;)) <> &#8216;0000-00-00&#8217;;
  </p>
  
  <p>
    ALTER TABLE `Spills` CHANGE `IncidentCompleteDate` `IncidentCompleteDate` DATE NULL DEFAULT NULL;
  </p>
  
  <p>
    UPDATE Spills<br /> SET ReleaseCleanupDate = DATE(STR_TO_DATE(ReleaseCleanupDate, &#8216;%m/%d/%Y&#8217;))<br /> WHERE DATE(STR_TO_DATE(ReleaseCleanupDate, &#8216;%m/%d/%Y&#8217;)) <> &#8216;0000-00-00&#8217;;
  </p>
  
  <p>
    ALTER TABLE `Spills` CHANGE `ReleaseCleanupDate` `ReleaseCleanupDate` DATE NULL DEFAULT NULL;
  </p>
  
  <p>
    [/code]
  </p>
  
  <p>
    There is also an issue with inconsistent units. Some entries have units of &#8220;m3&#8221;, and others are in units of &#8220;103m3&#8221;. Now it&#8217;s obviously not the case that the units are multiples of 103 in m<sup>3</sup>, but rather in 10<sup>3</sup> m<sup>3</sup>. In order for the volume filter to be implemented correctly, we&#8217;ll want consistent units:
  </p>
  
  <p>
    [code language=&#8221;sql&#8221;]<br /> UPDATE Spills SET  `Volume Released` = `Volume Released`*1000 WHERE `Volume Units`="103m3";<br /> UPDATE Spills SET  `Volume Recovered` = `Volume Recovered`*1000 WHERE `Volume Units`="103m3";
  </p>
  
  <p>
    UPDATE Spills SET `Volume Released 2` = `Volume Released 2`*1000 WHERE `Volume Units 2`="103m3";<br /> UPDATE Spills SET `Volume Recovered 2` = `Volume Recovered 2`*1000 WHERE `Volume Units 2`="103m3";
  </p>
  
  <p>
    UPDATE Spills SET `Volume Released 3` = `Volume Released 3`*1000 WHERE `Volume Units 3`="103m3";<br /> UPDATE Spills SET `Volume Recovered 3` = `Volume Recovered 3`*1000 WHERE `Volume Units 3`="103m3";
  </p>
  
  <p>
    UPDATE Spills SET `Volume Released 4` = `Volume Released 4`*1000 WHERE `Volume Units 4`="103m3";<br /> UPDATE Spills SET `Volume Recovered 4` = `Volume Recovered 4`*1000 WHERE `Volume Units 4`="103m3";<br /> [/code]
  </p>
  
  <p>
    That takes care of differing units, so now we don&#8217;t really need those units columns, since everything is in m<sup>3</sup> now.
  </p>
  
  <p>
    [code language=&#8221;sql&#8221;]<br /> ALTER TABLE `Spills`<br /> DROP `Volume Units`,<br /> DROP `Volume Units 2`,<br /> DROP `Volume Units 3`,<br /> DROP `Volume Units 4`;<br /> [/code]
  </p>
  
  <p>
    As this table isn&#8217;t going to be updated often (if at all), we&#8217;ll want to index anything that will be used as a search parameter.
  </p>
  
  <p>
    [code language=&#8221;sql&#8221;]
  </p>
  
  <p>
    ALTER TABLE `Spills` ADD INDEX( `Latitude`, `Longitude`, `IncidentDate`, `LicenseeName`, `Source`, `Substance Released`, `Volume Released`);
  </p>
  
  <p>
    [/code]
  </p>
  
  <p>
    And there we have it, a database that should be ready for the web application that will sit on top of it.
  </p>
</div>

<div id="code">
  <h3>
    The Code:
  </h3>
  
  <p>
    <a href="http://everettsprojects.com/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/"><em>There is an updated version of this project with a number of improvements.</em></a>
  </p>
  
  <p>
    If you just want a copy of all the files necessary (for version 1), then I have them <a href="http://everett.x10.mx/spillsv1/spills.zip">all in a zipped archive</a>. Don&#8217;t forget to go in and change the values of config.inc.php to reflect your own MySQL database.
  </p>
  
  <p>
    For everyone else, lets take a closer look at the code that makes it all work, starting with the JavaScript laden index.html file:
  </p>
  
  <div id="index">
    <p>
      [code language=&#8221;javascript&#8221; htmlscript=&#8221;true&#8221; title=&#8221;index.html&#8221; collapse=&#8221;true&#8221;]<br /> <!DOCTYPE html><br /> <html><br /> <head><br /> <meta name="viewport" content="initial-scale=1.0, user-scalable=no"><br /> <meta charset="utf-8"><br /> <title>Alberta Oil and Gas Incidents 1975 &#8211; 2013</title><br /> <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css"><br /> <link href="/spills/default.css" rel="stylesheet"><br /> <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script><br /> <script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script><br /> <script type="text/javascript"<br /> src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCIxpXOSPJWNG7TnhMYq-Q2hPcM7zEQs8g&sensor=false"><br /> </script><br /> <script><br /> //Make a bunch of variables to track the filters and map boundaries<br /> var sqlParameters = {<br /> currentSubstance : &#8216;All&#8217;,<br /> currentSource : &#8216;All&#8217;,<br /> currentLicensee: &#8216;All&#8217;,<br /> yearMin : 1975,<br /> yearMax : 2013,<br /> volumeMin : 0,<br /> volumeMax : 37000000,<br /> latMin : 0,<br /> latMax : 0,<br /> lngMin : 0,<br /> lngMax : 0<br /> }
    </p>
    
    <p>
      /////////////////////////////////////<br /> //Nice control widgets from jQueryUI:<br /> /////////////////////////////////////
    </p>
    
    <p>
      //Popup dialog window for disclaimer<br /> $(function() {<br /> $( "#disclaimer" ).dialog({<br /> autoOpen: false<br /> });
    </p>
    
    <p>
      $( "#disclaimer-opener" ).click(function() {<br /> $( "#disclaimer" ).dialog( "open" );<br /> });<br /> });
    </p>
    
    <p>
      //Popup dialog window for license<br /> $(function() {<br /> $( "#license" ).dialog({<br /> autoOpen: false,<br /> width: 350<br /> });
    </p>
    
    <p>
      $( "#license-opener" ).click(function() {<br /> $( "#license" ).dialog( "open" );<br /> });<br /> });
    </p>
    
    <p>
      //No data fetched dialog<br /> $(function() {<br /> $("#no-data").dialog({<br /> height: 80,<br /> autoOpen: false,<br /> dialogClass: &#8216;noTitleDialog&#8217;,<br /> open: function(event, ui){<br /> setTimeout("$(&#8216;#no-data&#8217;).dialog(&#8216;close&#8217;)",3000);<br /> }<br /> });<br /> });
    </p>
    
    <p>
      //Sliders<br /> $(function () {<br /> $(".slider").each(function () {<br /> var begin = $(this).data("begin"),<br /> end = $(this).data("end"),<br /> step = $(this).data("step");
    </p>
    
    <p>
      $(this).slider({<br /> range: "true",<br /> values: [begin, end],<br /> min: begin,<br /> max: end,<br /> step: step,<br /> slide: function (event, ui) {<br /> //Update text box quantity when the slider changes<br /> var sliderlow = ("#" + $(this).attr("id") + "_amount_low");<br /> $(sliderlow).val(ui.values[0]);
    </p>
    
    <p>
      var sliderhigh = ("#" + $(this).attr("id") + "_amount_high");<br /> $(sliderhigh).val(ui.values[1]);<br /> },<br /> //When the slider changes, update the displayed spills<br /> change: function(event, ui) {<br /> if ($(this).attr("id") == "years") {<br /> sqlParameters.yearMin = ui.values[0];<br /> sqlParameters.yearMax = ui.values[1];<br /> } else if ($(this).attr("id") == "volume") {<br /> sqlParameters.volumeMin = ui.values[0];<br /> sqlParameters.volumeMax = ui.values[1];<br /> }<br /> getSpills();<br /> }<br /> })
    </p>
    
    <p>
      //Initialize the text box quantity<br /> var sliderlow = ("#" + $(this).attr("id") + "_amount_low");<br /> $(sliderlow).val($(this).slider("values", 0));
    </p>
    
    <p>
      var sliderhigh = ("#" + $(this).attr("id") + "_amount_high");<br /> $(sliderhigh).val($(this).slider("values", 1));<br /> })
    </p>
    
    <p>
      //When the text box is changed, update the slider<br /> $(&#8216;.amount1&#8217;).change(function () {<br /> var value = this.value,<br /> selector = $("#" + this.id.split(&#8216;_&#8217;)[0]);<br /> selector.slider("values", 0, value);<br /> })<br /> $(&#8216;.amount2&#8217;).change(function () {<br /> var value = this.value,<br /> selector = $("#" + this.id.split(&#8216;_&#8217;)[0]);<br /> selector.slider("values", 1, value);<br /> })<br /> });
    </p>
    
    <p>
      //Accordian divs<br /> $(function() {<br /> $( "#accordion" ).accordion({<br /> collapsible: true,<br /> autoHeight: false,<br /> heightStyle: "content"<br /> });<br /> });
    </p>
    
    <p>
      //Get the Licensee list for the autocomplete widget<br /> var licenseeList = [];<br /> $.ajax({<br /> async: false,<br /> url : "getLicensees.php",<br /> dataType : "json",<br /> success: function(data){<br /> licenseeList = data;<br /> },<br /> error: function (data)<br /> {<br /> alert("Couldn&#8217;t retrieve the licensee list. A page refresh will usually fix this.");<br /> }<br /> });
    </p>
    
    <p>
      //Auto Complete Licensee Selector<br /> $(function() {<br /> var cache = [];<br /> $( "#licensee-selector" ).autocomplete({<br /> minLength: 2,<br /> source: licenseeList,<br /> select: function( event, ui ) {<br /> sqlParameters.currentLicensee = ui.item.value;<br /> getSpills();<br /> }<br /> });
    </p>
    
    <p>
      $( "#licensee-clear" ).click(function() {<br /> $( "#licensee-selector" ).val("");<br /> sqlParameters.currentLicensee = &#8216;All&#8217;;<br /> getSpills();<br /> });
    </p>
    
    <p>
      });
    </p>
    
    <p>
      //Drop down menus<br /> $(function() {<br /> $( "#substance-menu, #source-menu" ).menu();<br /> });
    </p>
    
    <p>
      //When the DOM is loaded, we want to configure stuff like the menus<br /> $( document ).ready(function() {<br /> makeMenus();
    </p>
    
    <p>
      //A hackish way to set the spill-info content max height based on window height<br /> document.getElementById("spill-info").style.maxHeight = $(window).height()*0.40 + "px";
    </p>
    
    <p>
      });
    </p>
    
    <p>
      //Build the menus after the window has loaded (This is called at the end of <body>)<br /> function makeMenus() {
    </p>
    
    <p>
      //Get the substances and sources for the filter menus<br /> var substanceList = [];<br /> $.ajax({<br /> async: false,<br /> url : "getSubstances.php",<br /> dataType : "json",<br /> success: function(data){<br /> substanceList = data;<br /> //replace the initial null element<br /> substanceList[0] = "All";<br /> },<br /> error: function (data)<br /> {<br /> alert("Couldn&#8217;t retrieve the substance list. A page refresh will usually fix this.");<br /> }<br /> });
    </p>
    
    <p>
      //And the Sources too<br /> var sourceList = [];<br /> $.ajax({<br /> async: false,<br /> url : "getSources.php",<br /> dataType : "json",<br /> success: function(data){<br /> sourceList = data;<br /> //replace the initial null element<br /> sourceList[0] = "All";<br /> },<br /> error: function (data)<br /> {<br /> alert("Couldn&#8217;t retrieve the source list. A page refresh will usually fix this.");<br /> }<br /> });
    </p>
    
    <p>
      //Build the lists using the database results<br /> //Function courtesy of http://stackoverflow.com/questions/11128700/create-a-ul-and-fill-it-based-on-a-passed-array<br /> function constructLI(domID, array) {
    </p>
    
    <p>
      var fieldID = (domID.split("-"))[0]+"-selected";
    </p>
    
    <p>
      for(var i = 0; i < array.length; i++) {<br /> // Create the list item:<br /> var member = document.createElement(&#8216;li&#8217;);
    </p>
    
    <p>
      // Set its contents:<br /> var linkText = document.createTextNode(array[i]);<br /> var link = document.createElement(&#8216;a&#8217;);<br /> link.appendChild(linkText);<br /> link.href= "#";<br /> link.title= linkText;
    </p>
    
    <p>
      //Make the onclick aspect of them menu work<br /> link.onclick = function() { setText( fieldID, this.firstChild.nodeValue ) };
    </p>
    
    <p>
      member.appendChild(link);
    </p>
    
    <p>
      // Add it to the list:<br /> document.getElementById(domID).appendChild(member);<br /> }<br /> }<br /> constructLI("substance-links", substanceList);<br /> constructLI("source-links", sourceList);<br /> }
    </p>
    
    <p>
      //Set the drop down menu to reflect the new filter value and update the displayed results<br /> function setText(domID, text) {<br /> document.getElementById(domID).innerHTML = text;<br /> if (domID == "substance-selected") {<br /> sqlParameters.currentSubstance = text;<br /> } else if (domID == "source-selected") {<br /> sqlParameters.currentSource = text;<br /> }<br /> getSpills();<br /> };
    </p>
    
    <p>
      //////////////////////////////<br /> //Start the Google Maps stuff<br /> //////////////////////////////
    </p>
    
    <p>
      var map;<br /> var markers = [];<br /> var selectedMarker = new google.maps.Marker({<br /> position: null,<br /> icon: &#8216;spotlight-poi.png&#8217;,<br /> map: map,<br /> spillID: null<br /> });<br /> var spillLocations;
    </p>
    
    <p>
      //Initialize when the map is done<br /> google.maps.event.addDomListener(window, &#8216;load&#8217;, initialize);
    </p>
    
    <p>
      function initialize() { clearStyle: true;<br /> var middleEarth = new google.maps.LatLng(54.5, -115.0);<br /> var mapOptions = {<br /> zoom: 6,<br /> center: middleEarth,<br /> mapTypeId: google.maps.MapTypeId.ROADMAP<br /> };
    </p>
    
    <p>
      map = new google.maps.Map(document.getElementById(&#8216;map-canvas&#8217;), mapOptions);
    </p>
    
    <p>
      makeGetSpillsEvent();<br /> }
    </p>
    
    <p>
      function makeGetSpillsEvent(){<br /> google.maps.event.addListener(map, &#8216;idle&#8217;, function() { getSpills();} );<br /> }
    </p>
    
    <p>
      function getSpills() {<br /> var mapCorners = map.getBounds();<br /> var ne = mapCorners.getNorthEast(); // LatLng of the north-east corner<br /> var sw = mapCorners.getSouthWest(); // LatLng of the south-west corder
    </p>
    
    <p>
      sqlParameters.latMin = sw.lat();<br /> sqlParameters.latMax = ne.lat();<br /> sqlParameters.lngMin = sw.lng();<br /> sqlParameters.lngMax = ne.lng();
    </p>
    
    <p>
      var newSpillLocations;
    </p>
    
    <p>
      //Get the spill location data<br /> $.ajax({<br /> url : "getSpillLocations.php",<br /> type: "POST",<br /> data : sqlParameters,<br /> dataType : "json",<br /> success: function(data){<br /> SpillLocations = data;<br /> plotSpills(SpillLocations);<br /> },<br /> error: function (data)<br /> {<br /> $( "#no-data" ).dialog( "open" );<br /> }<br /> });<br /> }
    </p>
    
    <p>
      function plotSpills(spillLocations){<br /> map.clearMarkers(markers);<br /> markers = [];<br /> markers.push(selectedMarker);<br /> //Stick those markers into the map canvas<br /> for (var i = 0; i < spillLocations.length; i++) {<br /> //Dont duplicate the selected marker.<br /> if (selectedMarker.spillID !== spillLocations[i].IncidentNumber) {<br /> var marker = new google.maps.Marker({<br /> position: new google.maps.LatLng(spillLocations[i].Latitude, spillLocations[i].Longitude),<br /> icon: &#8216;spotlight-poi.png&#8217;,<br /> map: map,<br /> spillID: spillLocations[i].IncidentNumber<br /> });<br /> }
    </p>
    
    <p>
      makeLoadSpillInfoEvent(marker);
    </p>
    
    <p>
      markers.push(marker);<br /> }<br /> }
    </p>
    
    <p>
      //The info window function from http://jsfiddle.net/yV6xv/161/<br /> function makeLoadSpillInfoEvent(marker) {<br /> google.maps.event.addListener(marker, &#8216;click&#8217;, function() {<br /> //Set the old marker back to red<br /> selectedMarker.setIcon(&#8216;spotlight-poi.png&#8217;);<br /> //Set the new marker to orange<br /> selectedMarker = marker;<br /> selectedMarker.setIcon(&#8216;spotlight-poi-orange.png&#8217;);<br /> loadSpillInfo(marker.spillID);<br /> });<br /> }
    </p>
    
    <p>
      //A function that fetches the specific spill info and loads it into the spill-info div<br /> function loadSpillInfo(spillID) {
    </p>
    
    <p>
      var spillInfo = {}
    </p>
    
    <p>
      $.ajax({<br /> async: false,<br /> url : "getSpillInfo.php",<br /> type: "POST",<br /> data: {&#8216;incidentnumber&#8217;:spillID},<br /> dataType : "json",<br /> success: function(data){<br /> spillInfo = data;<br /> },<br /> error: function (data)<br /> {<br /> $( "#no-data" ).dialog( "open" );<br /> }<br /> });
    </p>
    
    <p>
      //Clear existing content<br /> document.getElementById("spill-info").innerHTML = "";<br /> var table = document.createElement(&#8216;table&#8217;);
    </p>
    
    <p>
      //Populated the new table element<br /> for (var key in spillInfo) {<br /> if (spillInfo.hasOwnProperty(key)) {<br /> var row = document.createElement(&#8216;tr&#8217;);<br /> row.style.backgroundColor = "#ffebb8";<br /> var cell1 = row.insertCell(0);<br /> cell1.innerHTML = &#8216;<strong>&#8217;+key+'</strong>&#8217;;<br /> var cell2 = row.insertCell(1);<br /> cell2.innerHTML = spillInfo[key];<br /> table.appendChild(row);<br /> }<br /> }
    </p>
    
    <p>
      //Put the table into the div and open the spill info accordion section<br /> document.getElementById("spill-info").appendChild(table);<br /> $(&#8216;#accordion&#8217;).accordion("option", "active", 1);<br /> }
    </p>
    
    <p>
      //A customized clearOverlays function to remove the defunct markers but keep the selected one.<br /> google.maps.Map.prototype.clearMarkers = function() {<br /> for (var i = 0; i < markers.length; i++ ) {<br /> //Dont kill the selected marker, we want it to persist<br /> if (!(markers[i] === selectedMarker)) {<br /> markers[i].setMap(null);<br /> }<br /> }<br /> }<br /> </script><br /> </head><br /> <body><br /> <div id="map-canvas" style="width:100%;height:100%;"></div><br /> <div id="info-panel" style="text-align:left;"><br /> <div class="text-block"><br /> <h3>Alberta Oil and Gas Incidents 1975 &#8211; 2013</h3><br /> This is a map that interactively graphs all of the Oil and Gas related spills in alberta between the years 1975 and 2013. It is based on the data acquired by <a href="http://globalnews.ca/news/622513/open-data-alberta-oil-spills-1975-2013/" target="blank">Global News</a> from the <a href="http://en.wikipedia.org/wiki/Energy_Resources_Conservation_Board" target="blank">ERCB</a> (now the <a href="http://www.aer.ca/" target="blank">AER</a>).<br /> </br><br /> </br><br /> For optimal loading speeds and a clean map, it caps the number of incidents displayed to the 100 biggest spills (by volume in m<sup>3</sup>) in the current map area. Try zooming in to see more spills, or play with the provided filters to see more incidents.<br /> </br><br /> <p><br /> Learn more about this project at:<br /> <a href="http://everettsprojects.com/2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/" target="blank">everettsprojects.com</a><br /> </p><br /> </div><br /> <div id="accordion"><br /> <h3>Filter the Results</h3><br /> <div id="filter-pane"><br /> <p><br /> <label for="amount">Years:</label><br /> <span style="float:right;"><br /> <input type="text" class="amount1" id="years_amount_low" size="4"><br /> <span class="orange-text"> &#8211; </span><br /> <input type="text" class="amount2" id="years_amount_high" size="4"><br /> </span><br /> </p>
    </p>
    
    <p>
      <div class="slider" id="years" data-begin="1975" data-end="2013" data-step="1"> </div>
    </p>
    
    <p>
      <p><br /> <label for="amount">Volume:</label><br /> <span style="float:right;"><br /> <input type="text" class="amount1" id="volume_amount_low" size="9"><br /> <span class="orange-text"> &#8211; </span><br /> <input type="text" class="amount2" id="volume_amount_high" size="9"><br /> <span class="orange-text"> m<sup>3</sup></span><br /> </span><br /> </p>
    </p>
    
    <p>
      <div class="slider" id="volume" data-begin="0" data-end="37000000" data-step="1000"> </div><br /> <br><br /> <p><br /> <div class="ui-widget"><br /> <label for="licensee-selector">Company: </label><br /> <input id="licensee-selector" size="29" class="orange-text"> <span style="float:right;">[<a href=# id="licensee-clear">X</a>]</span><br /> <br><br /> </div><br /> </p>
    </p>
    
    <p>
      <p><br /> <ul id="substance-menu"><br /> <li><a href="#">Substance: <span id="substance-selected" class="orange-text">All</span></a><br /> <ul id="substance-links">
    </p>
    
    <p>
      </ul><br /> </li><br /> </ul><br /> </p><br /> <p><br /> <ul id="source-menu"><br /> <li><a href="#">Source: <span id="source-selected" class="orange-text">All</span></a><br /> <ul id="source-links">
    </p>
    
    <p>
      </ul><br /> </li><br /> </ul><br /> </p><br /> </div><br /> <h3>Incident Details</h3><br /> <div id="spill-info"><br /> This is where the data for a selected spill will be displayed. Click one to check it out!<br /> </div><br /> </div><br /> <div class="text-block"><br /> <p><br /> <a href="#" id="disclaimer-opener">Disclaimer</a> &#8211;<br /> <a href="#" id="license-opener">Copyright (c) 2014 Everett Robinson</a><br /> </p><br /> </div><br /> </div><br /> <div id="disclaimer" title="Disclaimer:" style="font-size:75%;"><br /> <p><br /> I do not under any circumstances guarantee the accuracy or truthfulness of the provided information. Furthermore, this project should not be taken as representative of the former ERCB, AER, or any other applicable parties.<br /> <br><br /> <br><br /> Due to the use of the Alberta Township System, many locations are approximations only. In general, points can be considered accurate to 200 metres.<br /> <br><br /> <br><br /> Any spills originating from trans-provincial or trans-national pipelines are not included, since they do not fall under the jursdiction of the AER. Furthermore, many spills under 2 m<sup>3</sup> that did not originate from a pipeline may be absent, as they are not required to be reported.<br /> </p><br /> </div><br /> <div id="license" title="MIT License:" style="font-size:75%;"><br /> <p><br /> Copyright (c) 2014 Everett Robinson<br /> </p><br /> <p><br /> This content is released under the MIT License.<br /> <br><br><br /> Permission is hereby granted, free of charge, to any person obtaining a copy<br /> of this software and associated documentation files (the "Software"), to deal<br /> in the Software without restriction, including without limitation the rights<br /> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell<br /> copies of the Software, and to permit persons to whom the Software is<br /> furnished to do so, subject to the following conditions:<br /> <br><br><br /> The above copyright notice and this permission notice shall be included in<br /> all copies or substantial portions of the Software.<br /> <br><br><br /> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR<br /> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,<br /> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE<br /> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER<br /> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,<br /> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN<br /> THE SOFTWARE.
    </p>
    
    <p>
      </p><br /> </div><br /> <div id="no-data" class="noTitleDialog" style="font-size:75%;"><br /> <p><br /> Oops, the spill locations or data couldn&#8217;t be loaded right now.<br /> </p><br /> </div><br /> </body><br /> </html><br /> [/code]
    </p>
  </div>
  
  <p>
    So that&#8217;s a bit of a long file, but I&#8217;ve tried to describe each function&#8217;s purpose, and have laid out the JavaScript as best as possible to provide a rational flow. Overall, the JavaScript is broken into 4 parts:
  </p>
  
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
  
  <p>
    There is then the HTML necessary for rendering the webpage, which relies on the following CSS file (default.css):
  </p>
  
  <div id="css">
    <p>
      [code language=&#8221;css&#8221; title=&#8221;default.css&#8221; collapse=&#8221;true&#8221;]<br /> html, body {<br /> background-color:#b0c4de;<br /> height: 100%;<br /> margin: 0;<br /> padding: 0;<br /> font-size: 100%;<br /> }
    </p>
    
    <p>
      #map-canvas, #map_canvas {<br /> height: 100%;<br /> }
    </p>
    
    <p>
      @media print {<br /> html, body {<br /> height: auto;<br /> }
    </p>
    
    <p>
      #map-canvas, #map_canvas {<br /> height: 650px;<br /> }<br /> }
    </p>
    
    <p>
      #info-panel {<br /> width: 25%;<br /> max-height: 96%;<br /> position: absolute;<br /> font-size: 75%;<br /> top: 10px;<br /> left: 90px;<br /> background-color: #fff;<br /> padding: 2px;<br /> border: 1px solid #999;<br /> background: rgba(255, 255, 255, 1);<br /> -webkit-border-radius: 5px;<br /> -moz-border-radius: 5px;<br /> -ms-border-radius: 5px;<br /> -o-border-radius: 5px;<br /> border-radius: 5px;<br /> border: outset 1px #a1b5cf;<br /> }
    </p>
    
    <p>
      .text-block {<br /> margin: 10px;<br /> border-width: 2px;<br /> text-align: center;<br /> }
    </p>
    
    <p>
      #accordion {<br /> margin: 10px;<br /> border-width: 2px;<br /> overflow: auto;<br /> }
    </p>
    
    <p>
      #filter-pane {<br /> overflow: auto;<br /> font-size: smaller;<br /> }
    </p>
    
    <p>
      .amount1, .amount2 {<br /> border: 0;<br /> color: #f6931f;<br /> font-weight: bold;<br /> text-align: center;<br /> }
    </p>
    
    <p>
      ul.ui-autocomplete {<br /> overflow: auto;<br /> width: 200px;<br /> max-height: 200px;<br /> font-size: 75%;
    </p>
    
    <p>
      }
    </p>
    
    <p>
      #substance-links {<br /> overflow: auto;<br /> width: 200px;<br /> max-height: 200px;<br /> z-index: 1;<br /> }
    </p>
    
    <p>
      #source-links {<br /> overflow: auto;<br /> width: 200px;<br /> max-height: 200px;<br /> z-index: 1;<br /> }
    </p>
    
    <p>
      .orange-text {<br /> color: #f6931f;<br /> font-weight:bold;<br /> }
    </p>
    
    <p>
      #spill-info {<br /> overflow: auto;<br /> font-size:smaller;<br /> max-height: 400px;<br /> }
    </p>
    
    <p>
      .noTitleDialog {<br /> text-align: center;<br /> }
    </p>
    
    <p>
      .noTitleDialog .ui-dialog-titlebar {<br /> display:none;<br /> }
    </p>
    
    <p>
      .ui-autocomplete-loading {<br /> background: white url(&#8216;images/ui-anim_basic_16x16.gif&#8217;) right center no-repeat;<br /> }<br /> [/code]
    </p>
  </div>
  
  <p>
    And Finally, six PHP files necessary for interfacing our web page to the database:
  </p>
  
  <div id="getSpillLocations">
    <p>
      [code language=&#8221;php&#8221; title=&#8221;getSpillLocations.php&#8221; collapse=&#8221;true&#8221;]<br /> <?php<br /> require(&#8216;config.inc.php&#8217;);
    </p>
    
    <p>
      //Get all of the POST data<br /> $currentlicensee = $_POST[&#8216;currentLicensee&#8217;];<br /> $currentsubstance = $_POST[&#8216;currentSubstance&#8217;];<br /> $currentsource = $_POST[&#8216;currentSource&#8217;];<br /> $yearmin = $_POST[&#8216;yearMin&#8217;];<br /> $yearmax = $_POST[&#8216;yearMax&#8217;];<br /> $volumemin = $_POST[&#8216;volumeMin&#8217;];<br /> $volumemax = $_POST[&#8216;volumeMax&#8217;];<br /> $latmin = $_POST[&#8216;latMin&#8217;];<br /> $latmax = $_POST[&#8216;latMax&#8217;];<br /> $longmin = $_POST[&#8216;lngMin&#8217;];<br /> $longmax = $_POST[&#8216;lngMax&#8217;];
    </p>
    
    <p>
      // Fix the years to go from start of first year to end of the last.<br /> $datemin = $yearmin."-01-01";<br /> $datemax = $yearmax."-12-31";
    </p>
    
    <p>
      //By using PDO and prepare, everything is automagically escaped<br /> $db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);
    </p>
    
    <p>
      //Start building the statement with the base of the query<br /> $stmtString = "SELECT `IncidentNumber`, `Latitude`, `Longitude` FROM `Spills` WHERE (((`Longitude` BETWEEN :longMin AND :longMax) AND (`Latitude` BETWEEN :latMin AND :latMax) AND (`IncidentDate` BETWEEN :dateMin AND :dateMax) AND (`Volume Released` BETWEEN :volumeMin AND :volumeMax))";
    </p>
    
    <p>
      //Add in the filters if they&#8217;re set<br /> if ($currentlicensee !== "All") {<br /> $stmtString .= " AND `LicenseeName` = :licensee";<br /> }<br /> if ($currentsubstance !== "All") {<br /> $stmtString .= " AND `Substance Released` = :substance";<br /> }<br /> if ($currentsource !== "All") {<br /> $stmtString .= " AND `Source` = :source";<br /> }
    </p>
    
    <p>
      //Finish the statement with the sorting and limit parts<br /> $stmtString .= ") ORDER BY `Volume Released` DESC LIMIT 100";
    </p>
    
    <p>
      //Bind all of the parameters<br /> $stmt = $db->prepare($stmtString);<br /> if (strpos($stmtString,&#8217;:licensee&#8217;) !== false) {<br /> $stmt->bindValue(&#8216;:licensee&#8217;, strval($currentlicensee), PDO::PARAM_STR);<br /> }<br /> if (strpos($stmtString,&#8217;:source&#8217;) !== false) {<br /> $stmt->bindValue(&#8216;:source&#8217;, strval($currentsource), PDO::PARAM_STR);<br /> }<br /> if (strpos($stmtString,&#8217;:substance&#8217;) !== false) {<br /> $stmt->bindValue(&#8216;:substance&#8217;, strval($currentsubstance), PDO::PARAM_STR);<br /> }<br /> $stmt->bindValue(&#8216;:latMin&#8217;, strval($latmin), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:latMax&#8217;, strval($latmax), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:longMin&#8217;, strval($longmin), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:longMax&#8217;, strval($longmax), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:dateMin&#8217;, strval($datemin), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:dateMax&#8217;, strval($datemax), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:volumeMin&#8217;, strval($volumemin), PDO::PARAM_STR);<br /> $stmt->bindValue(&#8216;:volumeMax&#8217;, strval($volumemax), PDO::PARAM_STR);<br /> $stmt->execute();
    </p>
    
    <p>
      //Get the results of the query<br /> $result;<br /> $result = $stmt->fetchAll(PDO::FETCH_ASSOC);<br /> //Spit out the results in json form<br /> echo header(&#8216;Content-type: application/json&#8217;);<br /> echo json_encode($result);<br /> ?><br /> [/code]
    </p>
  </div>
  
  <div id="getSpillInfo">
    <p>
      [code language=&#8221;php&#8221; title=&#8221;getSpillInfo.php&#8221; collapse=&#8221;true&#8221;]<br /> <?php
    </p>
    
    <p>
      $incidentNumber = $_POST[&#8216;incidentnumber&#8217;];
    </p>
    
    <p>
      require(&#8216;config.inc.php&#8217;);<br /> $db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);<br /> //By using PDO and prepare, everything is automagically escaped<br /> $stmt = $db->prepare("SELECT * FROM `Spills` WHERE `IncidentNumber` = :incidentNumber");<br /> $stmt->bindValue(&#8216;:incidentNumber&#8217;, strval($incidentNumber), PDO::PARAM_STR);<br /> /*** execute the prepared statement ***/<br /> $stmt->execute();<br /> $result = $stmt->fetch(PDO::FETCH_ASSOC);
    </p>
    
    <p>
      echo header(&#8216;Content-type: application/json&#8217;);<br /> echo json_encode($result);
    </p>
    
    <p>
      ?><br /> [/code]
    </p>
  </div>
  
  <div id="getLicensees">
    <p>
      [code language=&#8221;php&#8221; title=&#8221;getLicensees.php&#8221; collapse=&#8221;true&#8221;]<br /> <?php<br /> require(&#8216;config.inc.php&#8217;);
    </p>
    
    <p>
      $db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);<br /> //By using PDO and prepare, everything is automagically escaped<br /> $stmt = $db->prepare("SELECT `LicenseeName` FROM `Spills` GROUP BY `LicenseeName` ORDER BY `Spills`.`LicenseeName` ASC LIMIT 2000");<br /> $stmt->execute();<br /> $result = $stmt->fetchAll(PDO::FETCH_COLUMN, 0);
    </p>
    
    <p>
      echo header(&#8216;Content-type: application/json&#8217;);<br /> echo json_encode($result);
    </p>
    
    <p>
      ?><br /> [/code]
    </p>
  </div>
  
  <div id="getSubstances">
    <p>
      [code language=&#8221;php&#8221; title=&#8221;getSubstances.php&#8221; collapse=&#8221;true&#8221;]<br /> <?php<br /> require(&#8216;config.inc.php&#8217;);
    </p>
    
    <p>
      $db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);<br /> //By using PDO and prepare, everything is automagically escaped<br /> $stmt = $db->prepare("SELECT `Substance Released` FROM `Spills` GROUP BY `Substance Released` ORDER BY `Spills`.`Substance Released` ASC LIMIT 100");<br /> $stmt->execute();<br /> $result = $stmt->fetchAll(PDO::FETCH_NUM);
    </p>
    
    <p>
      echo header(&#8216;Content-type: application/json&#8217;);<br /> echo json_encode($result);
    </p>
    
    <p>
      ?><br /> [/code]
    </p>
  </div>
  
  <div id="getSources">
    <p>
      [code language=&#8221;php&#8221; title=&#8221;getSources.php&#8221; collapse=&#8221;true&#8221;]<br /> <?php<br /> require(&#8216;config.inc.php&#8217;);
    </p>
    
    <p>
      $db = new PDO("mysql:host=$dbhost;dbname=$dbname",$dbuser,$dbpass);<br /> //By using PDO and prepare, everything is automagically escaped, not that it&#8217;s necessary here<br /> $stmt = $db->prepare("SELECT `Source` FROM `Spills` GROUP BY `Source` ORDER BY `Spills`.`Source` ASC LIMIT 100");<br /> $stmt->execute();<br /> $result = $stmt->fetchAll(PDO::FETCH_NUM);
    </p>
    
    <p>
      echo header(&#8216;Content-type: application/json&#8217;);<br /> echo json_encode($result);
    </p>
    
    <p>
      ?><br /> [/code]
    </p>
  </div>
  
  <div id="config">
    <p>
      [code language=&#8221;php&#8221; title=&#8221;config.inc.php&#8221; collapse=&#8221;true&#8221;]<br /> <?php<br /> // These are the login credentials for your MySQL database,<br /> // don&#8217;t forget to set them.<br /> $dbhost = change me;<br /> $dbname = change me;<br /> $dbuser = change me;<br /> $dbpass = change me;<br /> ?>
    </p>
    
    <p>
      [/code]
    </p>
    
    <p>
      The first file, getSpillLocations.php, does what it sounds like. It takes all of the filter parameters along with the map boundaries, and then returns a JSON encoded list of coordinates and spill ID numbers to be plotted. The SQL statement is built based on the parameters passed, and then fulfilled using PHP Data Objects (PDO). The second, getSpillInfo.php, takes a spill ID number, and uses it to return all of the data for that spill as JSON object.<br /> The third, fourth, and fifth scripts are used to fetch lists from the database that are used to populate the menu widgets in the filter panel. They do not require any parameters to be passed, since they just return a list containing all of the existing values for each field. Finally, config.inc.php is simply a file containing the database access credentials, meant to be included in the five other scripts.
    </p>
  </div>
</div>

<div id="considerations">
  <h3>
    Considerations and Caveats:
  </h3>
  
  <p>
    The ERCB/AER uses the Alberta Township System (ATS) for reporting locations, which means the latitudes and longitudes in the database are converted values that represent the centre of the smallest unit in the ATS scheme; a Legal Sub-Division (LSD). Since a LSD is 400m along each side, it can be said that any plotted location is accurate to +/- 200m in each axis. This poses another problem however; certain legal subdivisions will have had multiple incidents on them in the 37 year period displayed. A great example is the region near Turner Valley:
  </p>
  
  <div id="attachment_999" style="width: 600px" class="wp-caption aligncenter">
    <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/06/spills-overlap-animation21.gif"><img class="wp-image-999 size-full" src="http://everett.x10.mx/wp/wp-content/uploads/2014/06/spills-overlap-animation21.gif" alt="spills-overlap-animation2" width="590" height="500" /></a>
    
    <p class="wp-caption-text">
      Overlapping spill incidents near Turner Valley need to be differentiated using the provided filters.
    </p>
  </div>
  
  <p>
    Here, several of the spills in this area were isolated using the provided filters. Unfortunately, there is not currently a mechanism to indicate that overlapping markers exist. The user will either need to have keen eyes to spot the signs, like a slight red border around the yellow selected marker, or play around with the filters to confirm any suspicions.
  </p>
  
  <p>
    Another consideration, which is not one I have control over is that any spills originating from trans-provincial or trans-national pipelines are not included, since they do not fall under the jurisdiction of the AER. Furthermore, many spills under 2 m<sup>3</sup> that did not originate from a pipeline may be absent, as they are not required to be reported.
  </p>
  
  <p>
    A final issue is that there are in fact 3 members of the database that do not possess a valid latitude or longitude; these fields are 0. The incident numbers are 19940377, 19850326, and 19871009 for reference. This means they are actually plotted in the south Atlantic, off the coast of Africa:
  </p>
  
  <div id="attachment_1004" style="width: 604px" class="wp-caption aligncenter">
    <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/06/spills-atlantic.png"><img class="size-full wp-image-1004" src="http://everett.x10.mx/wp/wp-content/uploads/2014/06/spills-atlantic.png" alt="These incidents are plotted in the wrong location at Latitude: 0, Longitude: 0" width="594" height="324" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills-atlantic.png 1440w, https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills-atlantic-300x163.png 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/06/spills-atlantic-1024x559.png 1024w" sizes="(max-width: 594px) 100vw, 594px" /></a>
    
    <p class="wp-caption-text">
      These incidents are plotted in the wrong location at Latitude: 0, Longitude: 0
    </p>
  </div>
  
  <p>
    Now, I could theoretically go in and correct the values for these three points by converting the ATS coordinates manually, but I decided not to since they illustrate an important point: None of the data in the database is vetted by me. I can not assure that any other data point is valid, though none of the rest are so obviously incorrect.
  </p>
  
  <p>
    So with those concerns out of the way; have fun exploring the often hushed side of the oil industry in Alberta.
  </p>
</div>