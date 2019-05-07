---
title: "Going Serverless: Has the world ended yet?"
author: "Everett Robinson"
date: "April 24, 2019"
output: html_document
layout: post
---


### Has the world ended yet?

This page contains a small amount of PHP embedded in it that pings google and returns no if it gets a response. 

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
{% endhighlight %}

This can be replaced with a trivial lambda function. Lambda functions don't support PHP, but we can use python instead to simply respond to the request. Really, it seems probable that if my lambda function isn't working, neither will the serving of my blog from an S3 bucket. So embedding this logic in a lambda function is little more than an exercise in the pointless, but so are the standard hello world lambda function examples elsewhere on the internet.

{% highlight python %}
import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps('No.')
    }
{% endhighlight %}

The lambda function and API Gateway were set up by following the steps in this [handy guide by Raju Dawadi](https://medium.com/@dwdraju/python-function-on-aws-lambda-with-api-gateway-endpoint-288eae7617cb).

The code for the new page, [everettsprojects.com/end-of-the-world.html](/end-of-the-world.html), now uses jquery in place of PHP and is fairly simple:

{% highlight html %}
<!DOCTYPE html>
<html>
  <script
    src="https://code.jquery.com/jquery-3.4.0.min.js"
    integrity="sha256-BJeo0qm959uMBGb65z40ejJYGSgR7REI4+CW1fNKwOg="
    crossorigin="anonymous">
  </script>

  <script>
  function succeeded(json){
    var str = json.body;
    var result = str.fontcolor("green");
    document.getElementById("result").innerHTML = result;
  }

  function failed(){
    var str = 'Yes!';
    var result = str.fontcolor("red");
    document.getElementById("result").innerHTML = result;
  }

  $.ajax({
    type: "GET",
    url: "https://vb7y770vle.execute-api.us-east-1.amazonaws.com/everettsprojects-production",
    dataType: "json",
    success: function (data) { 
      succeeded(data)
    },
    error: function() {
      failed()
    }
  });
  </script>

  <head>
    <title>Has the World Ended Yet?</title>
    <style>
      a:link {color:#FFFFFF;}
      a:visited {color:#FFFFFF;}

    html {
      overflow-y: scroll;
      background: url(/img/eow.jpg) no-repeat center center fixed;
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
        <b>
        <div id="result">
        </div>
        </b>
        <div id="disclaimer">
            <sup>*</sup> Does not actually check if the world has ended. Result is based on the assumption that if AWS is not responding, the world has probably ended. <br><br> <a href="http://everettsprojects.com">http://everettsprojects.com/</a>
        </div>
    </div>
</body>
</html>
{% endhighlight %}
