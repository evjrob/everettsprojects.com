---
id: 650
title: Has the world ended yet? A first attempt at web development
date: 2012-12-16T22:53:48+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=650
permalink: /2012/12/16/has-the-world-ended-yet-a-first-attempt-at-web-development/
tagazine-media:
  - 'a:7:{s:7:"primary";s:55:"http://ejrob.files.wordpress.com/2012/12/screenshot.png";s:6:"images";a:1:{s:55:"http://ejrob.files.wordpress.com/2012/12/screenshot.png";a:6:{s:8:"file_url";s:55:"http://ejrob.files.wordpress.com/2012/12/screenshot.png";s:5:"width";i:860;s:6:"height";i:516;s:4:"type";s:5:"image";s:4:"area";i:443760;s:9:"file_path";b:0;}}s:6:"videos";a:0:{}s:11:"image_count";i:1;s:6:"author";s:8:"15236702";s:7:"blog_id";s:8:"14753287";s:9:"mod_stamp";s:19:"2012-12-17 17:45:27";}'
twitter_cards_summary_img_size:
  - 'a:6:{i:0;i:860;i:1;i:516;i:2;i:3;i:3;s:24:"width="860" height="516"";s:4:"bits";i:8;s:4:"mime";s:9:"image/png";}'
dsq_thread_id:
  - "6140711573"
image: /wp-content/uploads/2014/07/screenshot-672x372.png
categories:
  - Programming
  - Web Applications
tags:
  - CSS3
  - Doomsday
  - End of World
  - HTML
  - PHP
  - web
  - Web Design
  - Web DevelopmentS
comments: true
---
Despite the sheer nuttiness of it, everyone keeps going on about the end of the world as &#8220;predicted&#8221; by the Mayan calendar. National Geographic even had and entire day devoted to it. Building on that theme, I decided to make a very convenient (and pretty much useless) [webpage](/end-of-the-world.html) that helps you figure out if the world has in fact ended: [http://everett.x10.mx/end-of-the-world.php](/end-of-the-world.html). This project was really simple, didn&#8217;t involve a lot of code or design, and was basically thrown together over the course of an hour and a half. It turns out PHP is extremely easy if your host is already configured for it, and I&#8217;m looking forward to doing some more web development related stuff both with PHP and other languages or tools. The HTML side of the page was also relatively straightforward. I&#8217;m impressed by what&#8217;s possible design wise using modern HTML and CSS3. My inspiration on that front was this amazing site: <http://www.tubalr.com/>

<p style="text-align:center;">
  <a href="end-of-the-world.php" rel="attachment wp-att-651"><img class="size-medium wp-image-651 aligncenter" alt="screenshot" src="/wp-content/uploads/2014/07/screenshot.png?w=300" width="600" height="360" /></a>
</p>

<p style="text-align:left;">
  It works as the page implies, by polling google.com for a response. If google is down, then it is assumed the world has ended, and the result is <span style="color:#000000;">&#8220;<span style="color:#ff0000;"><strong>Yes.</strong></span>&#8221; </span>in big red letters. The PHP that does the trick is a slightly modified version of what&#8217;s posted at the following site: <a href="http://css-tricks.com/snippets/php/check-if-website-is-available/">http://css-tricks.com/snippets/php/check-if-website-is-available/</a>. The background is not mine, but I&#8217;ve left attribution on the image, and you can find the originals here: <a href="http://m3-f.deviantart.com/gallery/?offset=24#/d3b4qgn">http://m3-f.deviantart.com/gallery/?offset=24#/d3b4qgn</a>.
</p>

<p style="text-align:left;">
  And because I see no reason not to release it, here is the entire source code for the page:
</p>

{% highlight php %}
<?php
   function Visit($url){
     $agent = "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)";$ch=curl_init();
     curl_setopt ($ch, CURLOPT_URL,$url );
     curl_setopt($ch, CURLOPT_USERAGENT, $agent);
     curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
     curl_setopt ($ch,CURLOPT_VERBOSE,false);
     curl_setopt($ch, CURLOPT_TIMEOUT, 5);
     curl_setopt($ch,CURLOPT_SSL_VERIFYPEER, FALSE);
     curl_setopt($ch,CURLOPT_SSLVERSION,3);
     curl_setopt($ch,CURLOPT_SSL_VERIFYHOST, FALSE);
     $page=curl_exec($ch);
     //echo curl_error($ch);
     $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
     curl_close($ch);
     if($httpcode>=200 && $httpcode<300) return true;
     else return false;
   }
   if (Visit("http://www.google.com")){
     $answer = "No.";
     $colour = "green";
   }
   else{
     $answer = "Yes.";
     $colour = "red";
   }
?>

<!DOCTYPE html>
<html>
  <head>
    <title>Has the World Ended Yet?</title>
<style>
  a:link {color:#FFFFFF;}
  a:visited {color:#FFFFFF;}

html {
  overflow-y: scroll;
  background: url(/backgrounds/eow.jpg) no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;

}

body {
  font-family: 'Open Sans', sans-serif;
  font-size: 24px;
  color: #fff;
  padding-bottom: 20px;
}

#main
{
  text-align: center;
  margin-top: 50px;
  margin-bottom: 20px;
  background: #000;
  background: rgba(0, 0, 0, 0.85);
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  -ms-border-radius: 5px;
  -o-border-radius: 5px;
  border-radius: 5px;
  -webkit-box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  -moz-box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  border: solid 1px #000;
  width:800px;
  margin-left:auto;
  margin-right:auto;
}
#result
{
  font-family: 'Open Sans', sans-serif;
  font-size: 112px;
  color: <?=$colour?>;
}

#disclaimer
{
  font-family: 'Open Sans', sans-serif;
  font-size: 12px;
  color: #fff;
  margin-top: 80px;
  margin-left: 100px;
  margin-right: 100px;
  margin-bottom: 50px;
}
</style>

  </head>
  <body>
    <div id="main">
        <H1>Has the world ended yet? <sup>*</sup></H1>
        <br>
        <div id="result">
            <b> <?=$answer?></b>
        </div>
        <div id="disclaimer">
            <sup>*</sup> Does not actually check if the world has ended. Result is based on the assumption that if Google.com is not responding, the world has probably ended. <br><br> <a href="/">http://everettsprojects.com/</a>
        </div>
    </div>
</body>
</html>
{% endhighlight %}
