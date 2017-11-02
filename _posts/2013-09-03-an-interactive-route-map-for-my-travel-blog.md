---
id: 840
title: An Interactive Route Map for my Travel Blog
date: 2013-09-03T23:38:55+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=840
permalink: /2013/09/03/an-interactive-route-map-for-my-travel-blog/
tagazine-media:
  - 'a:7:{s:7:"primary";s:54:"http://ejrob.files.wordpress.com/2013/09/travelmap.png";s:6:"images";a:1:{s:54:"http://ejrob.files.wordpress.com/2013/09/travelmap.png";a:6:{s:8:"file_url";s:54:"http://ejrob.files.wordpress.com/2013/09/travelmap.png";s:5:"width";i:1148;s:6:"height";i:789;s:4:"type";s:5:"image";s:4:"area";i:905772;s:9:"file_path";b:0;}}s:6:"videos";a:0:{}s:11:"image_count";i:1;s:6:"author";s:8:"15236702";s:7:"blog_id";s:8:"14753287";s:9:"mod_stamp";s:19:"2013-09-04 05:41:02";}'
image: /wp-content/uploads/2013/09/travelmap-672x372.png
categories:
  - Programming
  - Web Applications
tags:
  - Europe
  - Google Maps
  - HTML
  - javaScript
  - Map
  - Travel
  - web
  - Web Design
  - Web Development
comments: true
---
[<img class="aligncenter size-full wp-image-844" src="wp-content/uploads/2013/09/travelmap.png" alt="travelMap" width="594" height="408" srcset="/wp-content/uploads/2013/09/travelmap.png 1148w, /wp-content/uploads/2013/09/travelmap-300x206.png 300w, /wp-content/uploads/2013/09/travelmap-1024x703.png 1024w" sizes="(max-width: 594px) 100vw, 594px" />](http://everett.x10.mx/maps/)

See the finished project at: <https://everettsprojects.com/maps/>

For the last three months I have been on a backpacking trip, which is part of the reason why this blog has been so neglected for the past few months. A travel blog hosted at [meandmypack.wordpress.com](http://meandmypack.wordpress.com) had taken precedence, and I habitually kept that one updated throughout my trip. With all of that over though, I&#8217;ve had to find things to do in my time to keep my self from becoming bored and lethargic with life back home in Canada. One such activity is the tying up of loose ends as far as documentation of my trip is concerned, and from early on I had it in my mind to make a nice map of all the places I went. Over time this idea evolved into a whole project in it&#8217;s own right, using Google maps and becoming more interactive and feature rich every time my mind drifted back to the idea of it. I couldn&#8217;t really spare the time to design it while in Europe, and that probably would have been a waste of the limited time I had there any way. So I stored the idea away and made a promise to my self to figure it out back home. Now some two weeks later, I&#8217;ve pulled it off.

To start, I began with the Google Maps API v3 [Simple Polylines example code](https://developers.google.com/maps/documentation/javascript/examples/polyline-simple) and then added in [this code for adding in markers](http://jsfiddle.net/yV6xv/161/) to the map. The poly line consists of a large number of latitude and longitude coordinates that I fetched from Google maps using the LatLng Marker plugin available through Google Maps Labs. With a stubbornness that could be mistaken for OCD, I made sure the PolyLine at least vaguely resembled my true route between major destinations by routing them through all of the intermediate stations that the train called at along the way. This was accomplished with the travel report from my Eurail Pass ( I knew I diligently filled it out for a reason), and the [Eurail timetables](http://www.eurail.com/plan-your-trip/timetables). With these two tools, I could easily go back and find the true route of most of the train travel I did during my trip. Elsewhere when I didn&#8217;t travel by train I figured the route out through some combination of memory and Google. The markers for all of the main cities and attractions that I visited were simply made by selectively harvesting those coordinates from the Polyline list and then adding them to their own modified list with extra fields for the associated tag on my blog, and the blurb for the popup info box. I modified the marker code to put a link to the associated content on [meandmypack.wordpress.com](http://meandmypack.wordpress.com) inside that popup box.  Finally I felt that it would be nice to calculate the distance travelled from the Polyline, which I did with the [help of this code](https://groups.google.com/forum/#!topic/google-maps-js-api-v3/Op87g7lBotc).

With all of the main features of the map coded, and a few hours spent finding the geospatial coordinates of my route, I had a decent looking finished product. I spent just a little more time on the layout and design of the page so that some information about the map was presented in a permanent box in the top left hand corner. I&#8217;ve also decided to post the final draft of the code below for easy viewing by all interested parties:

#### index.html

{% highlight html %}
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Me and My Pack Interactive Route Map</title>
    <link href="/maps/default.css" rel="stylesheet">
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCIxpXOSPJWNG7TnhMYq-Q2hPcM7zEQs8g&sensor=false">
    </script>
    <script>
    //Standard Google Maps API code with project specific values
    function initialize() {
      var middleEarth = new google.maps.LatLng(52.01254, 8.2133);
      var mapOptions = {
        zoom: 5,
        center: middleEarth,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };

      var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

      //The Polyline coordinates. Lots and Lots of them.
      var routeCoordinates = [
          new google.maps.LatLng(51.51120, -0.11978),   //London
          new google.maps.LatLng(53.95795, -1.0934),
          new google.maps.LatLng(54.9681, -1.6173),
          new google.maps.LatLng(55.7743, -2.0110),
          new google.maps.LatLng(55.95324, -3.18827),   //Edinburgh
          new google.maps.LatLng(55.982, -3.616),
          new google.maps.LatLng(56.077, -3.923),
          new google.maps.LatLng(56.1387, -3.9179),     //Wallace monument
          new google.maps.LatLng(56.17843, -4.3821),    //Aberfoyle
          new google.maps.LatLng(56.23381, -4.4290),    //loch katrine
          new google.maps.LatLng(56.2440, -4.2158),
          new google.maps.LatLng(56.18932, -4.0510),    //doune
          new google.maps.LatLng(56.077, -3.923),
          new google.maps.LatLng(55.982, -3.616),
          new google.maps.LatLng(55.95324, -3.18827),   //Edinburgh
          new google.maps.LatLng(55.85931, -4.25836),
          new google.maps.LatLng(54.9617, -5.0142),
          new google.maps.LatLng(55.0317, -5.1047),
          new google.maps.LatLng(55.0271, -5.3356),
          new google.maps.LatLng(54.7595, -5.6473),
          new google.maps.LatLng(54.5971, -5.930),      //Belfast
          new google.maps.LatLng(54.852, -5.811),
          new google.maps.LatLng(54.982, -5.996),
          new google.maps.LatLng(55.058, -6.062),
          new google.maps.LatLng(55.200, -6.239),
          new google.maps.LatLng(55.24881, -6.48898),   //Giants causeway
          new google.maps.LatLng(54.745, -6.23),
          new google.maps.LatLng(54.5971, -5.930),      //Belfast
          new google.maps.LatLng(54.0011, -6.4129),
          new google.maps.LatLng(53.34980, -6.26028),   //Dublin
          new google.maps.LatLng(53.435, -7.941),
          new google.maps.LatLng(53.27055, -9.0566),    //Galway
          new google.maps.LatLng(53.271, -8.918),
          new google.maps.LatLng(53.207, -8.868),
          new google.maps.LatLng(53.139, -8.931),
          new google.maps.LatLng(53.114, -9.148),
          new google.maps.LatLng(53.016, -9.375),
          new google.maps.LatLng(52.97184, -9.42649),   //Cliffs of Moher
          new google.maps.LatLng(53.016, -9.375),
          new google.maps.LatLng(53.114, -9.148),
          new google.maps.LatLng(53.139, -8.931),
          new google.maps.LatLng(53.207, -8.868),
          new google.maps.LatLng(53.271, -8.918),
          new google.maps.LatLng(53.27055, -9.0566),    //Galway
          new google.maps.LatLng(53.435, -7.941),
          new google.maps.LatLng(53.34980, -6.26028),   //Dublin
          new google.maps.LatLng(53.3076, -4.6310),
          new google.maps.LatLng(53.204, -4.141),
          new google.maps.LatLng(53.287, -3.716),   
          new google.maps.LatLng(53.1968, -2.8798),
          new google.maps.LatLng(51.5901, -2.9984),
          new google.maps.LatLng(51.572, -2.649),
          new google.maps.LatLng(51.44877, -2.5800),
          new google.maps.LatLng(51.37737, -2.35709),       //Bath
          new google.maps.LatLng(51.0705, -1.8066),         //Salisbury
          new google.maps.LatLng(51.17885, -1.82618),       //Stonehenge
          new google.maps.LatLng(51.0705, -1.8066),         //Salisbury
          new google.maps.LatLng(51.53216, -0.12680),   //London
          new google.maps.LatLng(51.1086, 1.2870),
          new google.maps.LatLng(50.9143, 1.805),
          new google.maps.LatLng(50.62706, 3.0853),
          new google.maps.LatLng(50.8354, 4.3355),          //Brussels
          new google.maps.LatLng(51.2094, 3.2246),          //Bruges
          new google.maps.LatLng(50.8453, 4.3567),          //Brussels
          new google.maps.LatLng(51.2191, 4.421),       //Antwerp
          new google.maps.LatLng(51.809, 4.658),
          new google.maps.LatLng(52.0598, 4.3099),      //Den Haag
          new google.maps.LatLng(52.3879, 4.6386),      //Haarlem
          new google.maps.LatLng(52.3786, 4.9004),      //Amsterdam
          new google.maps.LatLng(52.3144, 5.113),
          new google.maps.LatLng(52.549, 5.639),
          new google.maps.LatLng(52.514, 6.079),        //Zwolle
          new google.maps.LatLng(53.2173, 6.564),       //Groningen
          new google.maps.LatLng(53.2316, 7.4657),
          new google.maps.LatLng(53.0827, 8.815),
          new google.maps.LatLng(53.5544, 10.005),      //Hamburg
          new google.maps.LatLng(53.8679, 10.6700),
          new google.maps.LatLng(54.502, 11.228),
          new google.maps.LatLng(54.652, 11.36),
          new google.maps.LatLng(54.7671, 11.8772),
          new google.maps.LatLng(55.6388, 12.0887),
          new google.maps.LatLng(55.6730, 12.564),      //Copenhagen
          new google.maps.LatLng(55.9155, 12.5007),
          new google.maps.LatLng(55.9641, 12.5333),     //Humlebaek
          new google.maps.LatLng(55.9155, 12.5007),
          new google.maps.LatLng(55.6730, 12.564),      //Copenhagen
          new google.maps.LatLng(55.6314, 12.6768),
          new google.maps.LatLng(55.5655, 12.8917),
          new google.maps.LatLng(55.7048, 13.1871),
          new google.maps.LatLng(56.0443, 12.6954),
          new google.maps.LatLng(56.5018, 12.9995),
          new google.maps.LatLng(56.6692, 12.8658),
          new google.maps.LatLng(57.7104, 11.9819),     //Gothenburg
          new google.maps.LatLng(58.2876, 12.2990),
          new google.maps.LatLng(58.9134, 11.9315),
          new google.maps.LatLng(58.9659, 11.552),
          new google.maps.LatLng(59.1206, 11.3859),
          new google.maps.LatLng(59.2857, 11.1183),
          new google.maps.LatLng(59.4319, 10.6565),
          new google.maps.LatLng(59.7195, 10.8347),
          new google.maps.LatLng(59.9095, 10.7598),     //Oslo
          new google.maps.LatLng(59.913, 10.626),
          new google.maps.LatLng(59.7407, 10.2042),
          new google.maps.LatLng(59.7616, 9.919),
          new google.maps.LatLng(60.052, 10.050),
          new google.maps.LatLng(60.1688, 10.2490),
          new google.maps.LatLng(60.4321, 9.4734),
          new google.maps.LatLng(60.6991, 8.9698),
          new google.maps.LatLng(60.6261, 8.5623),
          new google.maps.LatLng(60.5356, 8.2068),
          new google.maps.LatLng(60.4989, 8.0399),
          new google.maps.LatLng(60.5607, 7.5869),
          new google.maps.LatLng(60.6019, 7.5042),
          new google.maps.LatLng(60.7352, 7.1229),
          new google.maps.LatLng(60.6293, 6.4098),
          new google.maps.LatLng(60.5869, 5.8148),
          new google.maps.LatLng(60.455, 5.736),
          new google.maps.LatLng(60.3894, 5.3354),      //Bergen
          new google.maps.LatLng(60.455, 5.736),
          new google.maps.LatLng(60.5869, 5.8148),
          new google.maps.LatLng(60.6293, 6.4098),
          new google.maps.LatLng(60.7352, 7.1229),
          new google.maps.LatLng(60.6019, 7.5042),
          new google.maps.LatLng(60.6019, 7.5042),
          new google.maps.LatLng(60.5607, 7.5869),
          new google.maps.LatLng(60.4989, 8.0399),
          new google.maps.LatLng(60.5356, 8.2068),
          new google.maps.LatLng(60.6261, 8.5623),
          new google.maps.LatLng(60.6991, 8.9698),
          new google.maps.LatLng(60.4321, 9.4734),
          new google.maps.LatLng(60.1688, 10.2490),
          new google.maps.LatLng(60.052, 10.050),
          new google.maps.LatLng(59.7616, 9.919),
          new google.maps.LatLng(59.7407, 10.2042),
          new google.maps.LatLng(59.913, 10.626),
          new google.maps.LatLng(59.9095, 10.7598),     //Oslo
          new google.maps.LatLng(60.189, 12.005),
          new google.maps.LatLng(59.6533, 12.5912),
          new google.maps.LatLng(59.3776, 13.4994),
          new google.maps.LatLng(59.4182, 13.6920),
          new google.maps.LatLng(59.2292, 14.4394),
          new google.maps.LatLng(59.0668, 15.1098),
          new google.maps.LatLng(58.9964, 16.2101),
          new google.maps.LatLng(59.1790, 17.6459),
          new google.maps.LatLng(59.3311, 18.0551),     //Stockholm
          new google.maps.LatLng(59.3363, 18.2067),
          new google.maps.LatLng(59.3794, 18.2948),
          new google.maps.LatLng(59.3594, 18.4460),
          new google.maps.LatLng(59.3970, 18.4426),
          new google.maps.LatLng(59.4377, 18.3880),
          new google.maps.LatLng(59.4482, 18.4287),
          new google.maps.LatLng(59.4769, 18.4407),
          new google.maps.LatLng(59.5045, 18.479),
          new google.maps.LatLng(59.5757, 18.680),
          new google.maps.LatLng(59.7195, 19.115),
          new google.maps.LatLng(59.759, 19.319),
          new google.maps.LatLng(60.068, 19.925),
          new google.maps.LatLng(60.09231, 19.9279),
          new google.maps.LatLng(60.068, 19.925),
          new google.maps.LatLng(60.0130, 19.8542),
          new google.maps.LatLng(59.807, 19.878),
          new google.maps.LatLng(59.353, 22.72),
          new google.maps.LatLng(60.146, 25.001),
          new google.maps.LatLng(60.16780, 24.9528),    //Helsinki
          new google.maps.LatLng(52.51630, 13.37769),   //Berlin
          new google.maps.LatLng(51.0398, 13.7324),
          new google.maps.LatLng(50.901, 14.221),
          new google.maps.LatLng(50.7726, 14.2008),
          new google.maps.LatLng(50.6595, 14.0448),
          new google.maps.LatLng(50.5093, 14.0601),
          new google.maps.LatLng(50.0826, 14.4353),     //Prague
          new google.maps.LatLng(50.0309, 15.7563),
          new google.maps.LatLng(49.8967, 16.4462),
          new google.maps.LatLng(49.1898, 16.6130),
          new google.maps.LatLng(48.7545, 16.8954),
          new google.maps.LatLng(48.17483, 16.33662),   //Vienna
          new google.maps.LatLng(48.2082, 15.6257),
          new google.maps.LatLng(48.2896, 14.2928),
          new google.maps.LatLng(47.8129, 13.0470),
          new google.maps.LatLng(48.1405, 11.5569),     //Munich
          new google.maps.LatLng(47.9854, 10.1867),
          new google.maps.LatLng(47.54470, 9.6803),
          new google.maps.LatLng(47.5509, 9.7194),
          new google.maps.LatLng(47.5155, 9.7557),
          new google.maps.LatLng(47.5035, 9.7419),
          new google.maps.LatLng(47.4234, 9.3690),
          new google.maps.LatLng(47.5002, 8.7228),
          new google.maps.LatLng(47.3784, 8.5382),      //Zurich
          new google.maps.LatLng(47.2958, 8.5636),
          new google.maps.LatLng(47.1736, 8.5156),
          new google.maps.LatLng(47.1801, 8.4634),
          new google.maps.LatLng(47.0503, 8.3093),
          new google.maps.LatLng(46.762, 8.139),
          new google.maps.LatLng(46.7264, 8.1843),
          new google.maps.LatLng(46.7548, 8.0368),
          new google.maps.LatLng(46.6913, 7.8701),      //Interlaken
          new google.maps.LatLng(46.5989, 7.9081),
          new google.maps.LatLng(46.5753, 7.9390),
          new google.maps.LatLng(46.5844, 7.9601),
          new google.maps.LatLng(46.5745, 7.9742),      //Eiger trail
          new google.maps.LatLng(46.62418, 8.0337),
          new google.maps.LatLng(46.6328, 7.9009),
          new google.maps.LatLng(46.6913, 7.8701),      //Interlaken
          new google.maps.LatLng(46.7547, 7.6290),
          new google.maps.LatLng(46.9496, 7.4396),
          new google.maps.LatLng(46.8028, 7.1511),
          new google.maps.LatLng(46.5161, 6.6290),
          new google.maps.LatLng(46.5178, 6.5081),
          new google.maps.LatLng(46.3851, 6.2366),
          new google.maps.LatLng(46.21013, 6.1422),     //Geneva
          new google.maps.LatLng(45.9021, 6.1204),      //Annecy
          new google.maps.LatLng(45.6878, 5.9084),
          new google.maps.LatLng(45.802, 5.853),
          new google.maps.LatLng(45.95342, 5.3423),
          new google.maps.LatLng(45.7605, 4.8613),
          new google.maps.LatLng(43.9412, 4.8049),
          new google.maps.LatLng(43.6849, 4.6327),
          new google.maps.LatLng(43.5801, 4.9996),
          new google.maps.LatLng(43.4879, 5.2307),
          new google.maps.LatLng(43.3042, 5.3838),      //Marseille
          new google.maps.LatLng(43.4879, 5.2307),
          new google.maps.LatLng(43.5801, 4.9996),
          new google.maps.LatLng(43.6849, 4.6327),
          new google.maps.LatLng(43.8329, 4.3658),
          new google.maps.LatLng(43.6050, 3.8816),
          new google.maps.LatLng(43.3370, 3.2190),
          new google.maps.LatLng(43.1899, 3.0065),
          new google.maps.LatLng(42.544, 2.848),
          new google.maps.LatLng(42.2649, 2.9683),
          new google.maps.LatLng(41.9784, 2.8171),
          new google.maps.LatLng(41.7753, 2.7407),
          new google.maps.LatLng(41.548, 2.227),
          new google.maps.LatLng(41.3795, 2.1418),      //Barcelona
          new google.maps.LatLng(41.548, 2.227),
          new google.maps.LatLng(41.7753, 2.7407),
          new google.maps.LatLng(41.9784, 2.8171),
          new google.maps.LatLng(42.2649, 2.9683),
          new google.maps.LatLng(42.544, 2.848),
          new google.maps.LatLng(43.1899, 3.0065),
          new google.maps.LatLng(43.2172, 2.3502),
          new google.maps.LatLng(43.61116, 1.45425),
          new google.maps.LatLng(43.7035, 1.8137),
          new google.maps.LatLng(43.5995, 2.2302),      //Castres
          new google.maps.LatLng(43.7035, 1.8137),
          new google.maps.LatLng(43.61116, 1.45425),
          new google.maps.LatLng(44.0139, 1.3405),
          new google.maps.LatLng(44.2079, 0.6214),
          new google.maps.LatLng(44.8258, -0.5553),     //Bordeaux
          new google.maps.LatLng(44.6222, -1.002),
          new google.maps.LatLng(44.6585, -1.1653),
          new google.maps.LatLng(44.65592, -1.25991),   //Cap ferret
          new google.maps.LatLng(44.6585, -1.1653),
          new google.maps.LatLng(44.6222, -1.002),
          new google.maps.LatLng(44.8258, -0.5553),     //Bordeaux
          new google.maps.LatLng(44.9918, -0.440),
          new google.maps.LatLng(45.7482, -0.6182),
          new google.maps.LatLng(46.1528, -1.1431),
          new google.maps.LatLng(46.409, -0.892),
          new google.maps.LatLng(47.2182, -1.5363),
          new google.maps.LatLng(48.1027, -1.6725),     //Rennes
          new google.maps.LatLng(48.6357, -1.5112),     //Mont Saint Michel
          new google.maps.LatLng(48.1027, -1.6725),
          new google.maps.LatLng(47.99541, 0.1911),
          new google.maps.LatLng(48.8778, 2.3605),      //Paris gare de lest
          new google.maps.LatLng(49.2588, 4.0241),
          new google.maps.LatLng(49.1096, 6.1771),
          new google.maps.LatLng(49.5994, 6.1355),      //Luxembourg
          new google.maps.LatLng(49.1096, 6.1771),
          new google.maps.LatLng(48.5851, 7.7336),      //Strasbourg    
          new google.maps.LatLng(48.47824, 7.9475),
          new google.maps.LatLng(48.9936, 8.4013),
          new google.maps.LatLng(48.7848, 9.1827),      //Stuttgart
          new google.maps.LatLng(48.9936, 8.4013),
          new google.maps.LatLng(50.0507, 8.5709),
          new google.maps.LatLng(50.9433, 6.9587),      //Cologne
          new google.maps.LatLng(51.2196, 6.7936),
          new google.maps.LatLng(51.4291, 6.7765),
          new google.maps.LatLng(51.53123, 7.1659),
          new google.maps.LatLng(51.9564, 7.6352),
          new google.maps.LatLng(52.2759, 7.4342),
          new google.maps.LatLng(52.2092, 5.9692),
          new google.maps.LatLng(52.1541, 5.3728),
          new google.maps.LatLng(52.3786, 4.9004),      //Amsterdam
          new google.maps.LatLng(52.3879, 4.6386),      //Haarlem
          new google.maps.LatLng(52.0598, 4.3099),      //Den Haag
          new google.maps.LatLng(51.809, 4.658),
          new google.maps.LatLng(51.2191, 4.421),       //Antwerp
          new google.maps.LatLng(50.8453, 4.3567),          //Brussels
          new google.maps.LatLng(50.8354, 4.3355),          //Brussels
          new google.maps.LatLng(50.62706, 3.0853),
          new google.maps.LatLng(48.8822, 2.3563)       //Paris gare du nord
      ];

      var routePath = new google.maps.Polyline({
        path: routeCoordinates,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      //Use the Polyline to calculate the distance travelled for later
      document.getElementById("distanceTravelled").innerHTML = Math.round(routePath.inKm())+' km';

      //Add the Polyline to the map canvas
      routePath.setMap(map);

      //variables and list for the marker's to link back to the travel blog
      var tagURL = 'http://meandmypack.wordpress.com/tag/';

      var mainCities = [
          [51.51120, -0.11978, 'london', 'London'],
          [55.95324, -3.18827, 'edinburgh', 'Edinburgh'],
          [56.23381, -4.4290, 'highlands', 'Scottish Highlands'],
          [54.5971, -5.930, 'belfast', 'Belfast'],
          [55.24881, -6.48898, 'giants-causeway', 'Giant\'s Causeway'],
          [53.27055, -9.0566, 'galway', 'Galway'],
          [52.97184, -9.42649, 'cliffs-of-moher', 'Cliffs of Moher'],
          [53.34980, -6.26028, 'dublin', 'Dublin'],
          [51.37737, -2.35709, 'bath', 'Bath'],
          [51.0705, -1.8066, 'salisbury', 'Salisbury'],
          [51.17885, -1.82618, 'stonehenge', 'Stonehenge'],
          [51.2094, 3.2246, 'bruges', 'Bruges'],
          [50.8354, 4.3355, 'brussels', 'Brussels'],
          [52.3786, 4.9004, 'amsterdam', 'Amsterdam'],
          [53.2173, 6.564, 'groningen', 'Groningen'],
          [53.5544, 10.005, 'hamburg', 'Hamburg'],
          [55.6730, 12.564, 'copenhagen', 'Copenhagen'],
          [57.7104, 11.9819, 'gothenburg', 'Gothenburg'],
          [59.9095, 10.7598, 'oslo', 'Oslo'],
          [60.3894, 5.3354, 'bergen', 'Bergen'],
          [59.3311, 18.0551, 'stockholm', 'Stockholm'],
          [60.16780, 24.9528, 'helsinki', 'Helsinki'],
          [52.51630, 13.37769, 'berlin', 'Berlin'],
          [50.0826, 14.4353, 'prague', 'Prague'],
          [48.17483, 16.33662, 'vienna', 'Vienna'],
          [48.1405, 11.5569, 'munich', 'Munich'],
          [47.3784, 8.5382, 'zurich', 'Zurich'],
          [46.6913, 7.8701, 'interlaken', 'Interlaken'],
          [46.5745, 7.9742, 'eiger-trail', 'The Eiger Trail'],
          [45.9021, 6.1204, 'annecy', 'Annecy'],
          [43.3042, 5.3838, 'marseille', 'Marseille'],
          [41.3795, 2.1418, 'barcelona', 'Barcelona'],
          [43.5995, 2.2302, 'castres', 'Castres'],
          [44.8258, -0.5553, 'bordeaux', 'Bordeaux'],
          [44.65592, -1.25991, 'cap-ferret', 'Arcachon and Cap Ferret'],
          [48.1027, -1.6725, 'rennes', 'Rennes'],
          [48.6357, -1.5112, 'mont-saint-michel', 'Mont Saint Michel'],
          [49.5994, 6.1355, 'luxembourg', 'Luxembourg'],
          [48.5851, 7.7336, 'strasbourg', 'Strasbourg'],
          [48.7848, 9.1827, 'stuttgart', 'Stuttgart'],
          [50.9433, 6.9587, 'cologne', 'Cologne'],
          [52.3879, 4.6386, 'haarlem', 'Haarlem'],
          [48.8822, 2.3563, 'paris', 'Paris']         
      ];

      var markers = [];

      //Stick those markers into the map canvas
      for (var i = 0; i < mainCities.length; i++) {
        var marker = new google.maps.Marker({
          position: new google.maps.LatLng(mainCities[i][0], mainCities[i][1]),
          map: map
        });
        var infowindow = new google.maps.InfoWindow({
          content: '<a href="'+tagURL+mainCities[i][2]+'/" target="blank">'+mainCities[i][3]+'</a>'
        });

        makeInfoWindowEvent(map, infowindow, marker);

        markers.push(marker);
      }
    }

    //The info window function from http://jsfiddle.net/yV6xv/161/
    function makeInfoWindowEvent(map, infowindow, marker) {
      google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
      });
    }

    //The polyline distance code from https://groups.google.com/forum/#!topic/google-maps-js-api-v3/Op87g7lBotc
    google.maps.LatLng.prototype.kmTo = function(a){
          var e = Math, ra = e.PI/180;
          var b = this.lat() * ra, c = a.lat() * ra, d = b - c;
          var g = this.lng() * ra - a.lng() * ra;
          var f = 2 * e.asin(e.sqrt(e.pow(e.sin(d/2), 2) + e.cos(b) * e.cos(c) * e.pow(e.sin(g/2), 2)));
          return f * 6378.137;
    }

    google.maps.Polyline.prototype.inKm = function(n){
          var a = this.getPath(n), len = a.getLength(), dist = 0;
            for(var i=0; i<len-1; i++){
            dist += a.getAt(i).kmTo(a.getAt(i+1));
          }
          return dist;
    }


    google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>
  <body>
        <div id="map-canvas" style="float:left;width:100%;height:100%;"></div>
        <div id="info-panel" style="float:right;text-align:left;">
        <div style="margin:10px;border-width:2px;float:center;text-align:center;">
          <h3>Me and My Pack Interactive Route Map</h3>
          <b>Distance Travelled: </b>
          <div id="distanceTravelled"></div><br>
          <a href="http://meandmypack.wordpress.com" target="blank">meandmypack.wordpress.com</a><br>
          <a href="http://everettsprojects.com" target="blank">everettsprojects.com</a>
        </div>
  </body>
</html>
```

**default.css**
```css
html, body {
  background-color:#b0c4de;
  height: 100%;
  margin: 0;
  padding: 0;
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
  font-size: 12px;
  position: absolute;
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
{% endhighlight %}
