+++
title = "Going Serverless"
description = "A serverless blog architecture using a public website S3 bucket and AWS lambda functions to reduce hosting costs and make it easier to update with new content!"
date = "2019-05-20"
authors = [ "Everett Robinson",]
aliases = ["/2019/05/20/going-serverless.html"]

[extra]
layout = "post"
output = "html_document"
+++

### Why?

Back in 2017 I converted this blog from WordPress to Jekyll. It continues to run on the original web hosting I signed up for with WordPress, a service that is certainly overkill for a mostly static website. Really the only thing holding me back from moving this blog from my current provider to S3 on AWS are a few of my older projects that currently use PHP or databases on this web host.

These are:

1. [Has the world ended yet?](/end-of-the-world.html)
2. [Designing a secure(ish) login script with PHP and MySQL](/2013/02/17/designing-a-secureish-login-script-with-php-and-mysql/)
3. [Mapping Oil and Gas Incidents in Alberta with Google Maps, JQuery, and PHP](/2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/)
4. [Mapping Oil and Gas Incidents in Alberta: Improvements](/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/)


The first one is really simple. It uses PHP to check that google responds to a ping on the premise that if google is down, the world has probably ended. In 2019, it seems just as reasonable to assume that if AWS is down that the world has ended. And even if the world hasn't ended, [much of the internet probably has, at least temporarily](http://nymag.com/intelligencer/2018/03/when-amazon-web-services-goes-down-so-does-a-lot-of-the-web.html). And really that's the same thing, right?

The second is a PHP login script I decided to write while I was still an environmental science and physics undergrad. In the roughly six years since I launched it 192 accounts have been registered, five of which belong to me from initial testing. The majority of emails entered appear to be completely fake, since I never bothered to check them for validity. I really don't think it makes sense to maintain this database any longer, and no one should use my crumby PHP scripts for something so critical. I really don't like the idea of removing things from the internet, so my compromise will be to shut down the live demo, but keep the blog post and code available.

The third and fourth posts are worth keeping, and my intent is to move them to lambda functions. The usage of these pages is so low I don't expect them to cost anything at all. I'm only going to keep the improved serverless version of the map alive. The code for the older versions can always be found in the history of the associated git repository.

Going serverless has the potential to help me save a little money each year. By my calculations, running this little blog on AWS will cost me about \\$15 per year rather than the \\$60 I currently pay. This will be worth looking at more closely once I've actually built everything out and know the true costs.

### How?

As mentioned earlier, I plan to host this blog on AWS S3 going forward. Setting up an S3 bucket for this purpose is well documented, with  [official documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html) and [helpful tutorials](https://8thlight.com/blog/sarah-sunday/2018/02/14/making-a-static-website-with-jekyll-and-s3.html) to aid in the process.

The first step is to create a public S3 bucket for my blog, which is super simple in AWS. You literally just make an S3 bucket and then under the Properties tab of the bucket you select the Static Website Hosting option. Once that is complete you will want to adjust the bucket policy to allow public access:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket/*"
            ]
        }
    ]
}
```

The second step is to install the ruby gem s3_website. This gem unfortunately requires Java 8, and modern ubuntu ships with 11. The solution I found was to use the command [PATH=/usr/lib/jvm/java-8-openjdk-amd64/bin/:$PATH s3_website push](https://github.com/laurilehmijoki/s3_website/issues/300#issuecomment-446821789) to make sure s3_website finds the Java 8 environment. You will also need to create the s3_website.yml file with the command *s3_website cfg create* and at a minimum fill in the *s3_bucket: your-bucket-name* field. I also strongly recommend that you do not keep your AWS credentials in this file. Just store them in environment variables via *aws configure*.

The third step is to configure Route 53 on AWS, and have the [existing domain point to the new Route 53 name servers for the S3 bucket above](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-inactive.html).

That's really all there is to it. Updating my blog is now much simpler. I just need to build it with jekyll and run the s3_website push command above. If you're reading this now, it's on AWS S3! The following sections outline how I converted the has the world ended yet and Alberta spills map projects to serverless:

### Has the world ended yet?

This page contains a small amount of PHP embedded in it that pings google and returns no if it gets a response. 

```php
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
```

This can be replaced with a trivial lambda function. Lambda functions don't support PHP, but we can use python instead to simply respond to the request. Really, it seems probable that if my lambda function isn't working, neither will the serving of my blog from an S3 bucket. So embedding this logic in a lambda function is little more than a pointless exercise, but so are the standard hello world lambda function examples elsewhere on the internet.

```python
import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps('No.')
    }
```

The lambda function and API Gateway were set up by following the steps in this [handy guide by Raju Dawadi](https://medium.com/@dwdraju/python-function-on-aws-lambda-with-api-gateway-endpoint-288eae7617cb).

The code for the new page, [everettsprojects.com/end-of-the-world.html](/end-of-the-world.html), now uses jquery in place of PHP and is fairly simple:

```html
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
    url: "https://10phigl5s2.execute-api.us-east-1.amazonaws.com/Prod/hasworldended",
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
            <sup>*</sup> Does not actually check if the world has ended. Result is based on the assumption that if AWS is not responding, the world has probably ended. <br><br> <a href="/">http://everettsprojects.com/</a>
        </div>
    </div>
</body>
</html>
```

### Mapping Oil and Gas Incidents in Alberta

All of the code for the refactored Alberta Spills Map exists in the original [GitHub repository](https://github.com/evjrob/Alberta-Spills-Map) for the project.

#### Planning and Replanning

Refactoring this project to be serverless requires a little more effort than the simple end of the world page did, but not much. Originally I planned to migrate the data currently stored in a MySQL table to an AWS DynamoDB table. I hoped that translating the single relational table structure to a document database model would be as simple as creating a document for each row in the existing table, and then translating the queries from SQL to the appropriate forms for DynamoDB. I even got as far as populating the DynamoDB table with all of the records. Unfortunately this is where things began to break down. A novice with NoSQL databases, I didn't realized how much effort would be required to try and replicate easy query functions like SELECT DISTINCT, or LIMIT on the results of a query. For DynamoDB at least, the behaviour was that DISTINCT would require post processing by the lambda function after performing an expensive scan operation. LIMIT meanwhile exists in DynamoDB, but it appears to be the case that the query will first return only a number of records specified by limit, and then apply all the filtering steps in the query. This seems backwards to my old relational sensibilities, but I suppose it makes sense in the context of reducing expensive scans through the database.

I spent a couple days researching and dreaming up complicated schemes to try and fit the NoSQL shaped peg into the relational database shaped hole that is this problem. Many of these schemes involved parallel tables with pre-computed results that would help me avoid full scans, and they were really only feasible because of the fact that the underlying spills data is essentially never changing. It was this fact that the data is unchanging that lead me to the real solution: SQLite. It sounds kind of crazy, but it's really quite simple. Lambda functions allow you to provide a [deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) for when the function has dependencies that are not part of the standard AWS language deployment. Nominally, the limit for these deployment packages is 50MB, but [in practice it appears we can go much lager](https://hackernoon.com/exploring-the-aws-lambda-deployment-limits-9a8384b0bec3?gi=247504f61c03). This means a SQLite database of the Spills table, measuring in at 39.1MB is good to go. In fact when the whole lambda function is zipped for AWS it comes in at a tiny 8.7MB for each function.


#### The Database

I built the SQLite database from a "CSV" data dump of the MySQL database. I put CSV in quotes because in reality I have used a different delimiter \(\|\) to avoid issues with text columns in the CSV that contain commas. There are also some apostrophes in text columns which have been escaped as double apostrophes \(''\). With this file created, building the SQLite database is as simple as running the following statements within the SQLite console:

```sql
CREATE TABLE `Spills` (
  `IncidentNumber` INTEGER PRIMARY KEY,
  `IncidentType` TEXT DEFAULT NULL,
  `Latitude` REAL DEFAULT NULL,
  `Longitude` REAL DEFAULT NULL,
  `Location` TEXT DEFAULT NULL,
  `IncidentLSD` INTEGER DEFAULT NULL,
  `IncidentSection` INTEGER DEFAULT NULL,
  `IncidentTownship` INTEGER DEFAULT NULL,
  `IncidentRange` INTEGER DEFAULT NULL,
  `IncidentMeridian` INTEGER DEFAULT NULL,
  `LicenceNumber` TEXT DEFAULT NULL,
  `LicenceType` TEXT DEFAULT NULL,
  `IncidentDate` TEXT DEFAULT NULL,
  `IncidentNotificationDate` TEXT DEFAULT NULL,
  `IncidentCompleteDate` TEXT DEFAULT NULL,
  `Source` TEXT DEFAULT NULL,
  `CauseCategory` TEXT DEFAULT NULL,
  `CauseType` TEXT DEFAULT NULL,
  `FailureType` TEXT DEFAULT NULL,
  `StrikeArea` TEXT DEFAULT NULL,
  `FieldCentre` TEXT DEFAULT NULL,
  `LicenseeID` INTEGER(4) DEFAULT NULL,
  `LicenseeName` TEXT DEFAULT NULL,
  `InjuryCount` INTEGER DEFAULT NULL,
  `FatalityCount` INTEGER DEFAULT NULL,
  `Jurisdiction` TEXT DEFAULT NULL,
  `ReleaseOffsite` TEXT DEFAULT NULL,
  `SensitiveArea` TEXT DEFAULT NULL,
  `PublicAffected` TEXT DEFAULT NULL,
  `EnvironmentAffected` TEXT DEFAULT NULL,
  `WildlifeLivestockAffected` TEXT DEFAULT NULL,
  `AreaAffected` TEXT DEFAULT NULL,
  `PublicEvacuatedCount` INTEGER DEFAULT NULL,
  `ReleaseCleanupDate` TEXT DEFAULT NULL,
  `PipelineLicenceSegmentID` INTEGER DEFAULT NULL,
  `PipelineLicenceLineNo` INTEGER DEFAULT NULL,
  `PipeDamageType` TEXT DEFAULT NULL,
  `PipeTestFailure` TEXT DEFAULT NULL,
  `PipelineOutsideDiameter(mm)` REAL DEFAULT NULL,
  `PipeGrade` TEXT DEFAULT NULL,
  `PipeWallThickness(mm)` REAL DEFAULT NULL,
  `Substance Released` TEXT DEFAULT NULL,
  `Volume Released` REAL DEFAULT NULL,
  `Volume Recovered` REAL DEFAULT NULL,
  `Substance Released 2` TEXT DEFAULT NULL,
  `Volume Released 2` REAL DEFAULT NULL,
  `Volume Recovered 2` REAL DEFAULT NULL,
  `Substance Released 3` TEXT DEFAULT NULL,
  `Volume Released 3` REAL DEFAULT NULL,
  `Volume Recovered 3` REAL DEFAULT NULL,
  `Substance Released 4` TEXT DEFAULT NULL,
  `Volume Released 4` REAL DEFAULT NULL,
  `Volume Recovered 4` REAL DEFAULT NULL
);

CREATE INDEX spills_idx ON `Spills` (`Location`, `Latitude`, `Longitude`, 
  `IncidentDate`, `FailureType`, `LicenseeName`, `Source`, `InjuryCount`,
  `FatalityCount`, `Substance Released`, `Volume Released`);

.mode csv
.separator "|"
.import Spills.csv Spills
```


#### REST API Queries

One benefit of my otherwise unsuccessful experiments with DynamoDB is that I decided to export the results of the getLicensees.php, getSubstances.php, and getSources.php scripts to static JSON files. The data I use in this project is never changed or updated, and all these scripts do is return a static list of the unique values for their respective columns when the user first loads the page. User actions have no impact on their contents, and so there is really no reason to complicate things with a lambda function. It makes sense to just host the JSON file directly in S3 and have jQuery fetch that. Maybe someday the AER will make this spills database more public and I will update it regularly, but I'm not holding my breath given they haven't already done so in the six years since I created this project.

This leaves the getSpillLocations.php and getSpillInfo.php scripts to be converted to serverless equivalents. The getSpillLocations.php script returns the locations for the 100 largest spills given the current map view and filtering criteria. The getSpillInfo.php script returns all spills that pass the UI filters for a given location marker when it's clicked.

The get_spill_locations lambda function in python takes care of getSpillLocations.php:

```python
import json
import sqlite3


def get_spill_locations(long_min, long_max, lat_min, lat_max, date_min, date_max, 
                        volume_min, volume_max, injury_min, injury_max, 
                        fatality_min, fatality_max, licensee, substance, source, 
                        failure):
    # Database name in URI form, readonly
    database_name = "file:spills.db?mode=ro"

    # Create a database connection
    conn = sqlite3.connect(database_name, uri=True)
    
    with conn:
        cur = conn.cursor()

        # Start building the statement with the base of the query
        statement = "SELECT DISTINCT `Location`, `Latitude`, `Longitude` \
                     FROM Spills \
                     WHERE (((`Longitude` BETWEEN ? AND ?) \
                     AND (`Latitude` BETWEEN ? AND ?) \
                     AND (`IncidentDate` BETWEEN ? AND ?) \
                     AND (`Volume Released` BETWEEN ? AND ?) \
                     AND (`InjuryCount` BETWEEN ? AND ?) \
                     AND (`FatalityCount` BETWEEN ? AND ?))"

        statement_params = [long_min, long_max, lat_min, lat_max, \
                            date_min, date_max, volume_min, volume_max, \
                            injury_min, injury_max, fatality_min, fatality_max]

        # Add in the filters if they're set
        if (licensee != "All"):
            statement = statement + " AND `LicenseeName` = ?"
            statement_params = statement_params + [licensee]
        
        if (substance != "All"):
            statement = statement + " AND `Substance Released` = ?"
            statement_params = statement_params + [substance]
        
        if (source != "All"):
            statement = statement + " AND `Source` = ?"
            statement_params = statement_params + [source]
        
        if (failure != "All"):
            statement = statement + " AND `FailureType` = ?"
            statement_params = statement_params + [failure]

        

        # Finish the statement with the sorting and limit parts
        statement = statement + ") ORDER BY `Volume Released` DESC LIMIT 100"

        cur.execute(statement, tuple(statement_params))
        rows = cur.fetchall()

        def objectify(row):
            row_obj = {
                "Location":row[0],
                "Latitude":row[1],
                "Longitude":row[2]
            }
            return row_obj

        rows = [objectify(row) for row in rows]

        return rows
    

def lambda_handler(event, context):
    # Get all of the POST data
    licensee = event['currentLicensee']
    substance = event['currentSubstance']
    source = event['currentSource']
    failure = event['currentFailure']
    year_min = event['yearMin']
    year_max = event['yearMax']
    volume_min = event['volumeMin']
    volume_max = event['volumeMax']
    injury_min = event['injuryMin']
    injury_max = event['injuryMax']
    fatality_min = event['fatalityMin']
    fatality_max = event['fatalityMax']
    lat_min = event['latMin']
    lat_max = event['latMax']
    long_min = event['lngMin']
    long_max = event['lngMax']

    # Fix the years to go from start of first year to end of the last.
    date_min = str(year_min) + "-01-01"
    date_max = str(year_max) + "-12-31"

    result = get_spill_locations(long_min, long_max, lat_min, lat_max, date_min, \
        date_max, volume_min, volume_max, injury_min, injury_max, fatality_min, \
        fatality_max, licensee, substance, source, failure)
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True 
        },
        "body": result
    }

    # Spit out the results in json form
    return json.dumps(response)
```


And get_spill_info handles getSpillInfo.php:

```python
import json
import sqlite3


def get_spill_info(location, date_min, date_max, volume_min, volume_max, 
                   injury_min, injury_max, fatality_min, fatality_max,
                   licensee, substance, source, failure):
    # Database name in URI form, readonly
    database_name = "file:spills.db?mode=ro"

    # Create a database connection
    conn = sqlite3.connect(database_name, uri=True)
    
    with conn:
        cur = conn.cursor()

        # Start building the statement with the base of the query
        statement = "SELECT * \
                     FROM Spills \
                     WHERE ((`Location` = ? \
                     AND (`IncidentDate` BETWEEN ? AND ?) \
                     AND (`Volume Released` BETWEEN ? AND ?) \
                     AND (`InjuryCount` BETWEEN ? AND ?) \
                     AND (`FatalityCount` BETWEEN ? AND ?))"

        statement_params = [location, date_min, date_max, volume_min, volume_max,\
                            injury_min, injury_max, fatality_min, fatality_max]

        # Add in the filters if they're set
        if (licensee != "All"):
            statement = statement + " AND `LicenseeName` = ?"
            statement_params = statement_params + [licensee]
        
        if (substance != "All"):
            statement = statement + " AND `Substance Released` = ?"
            statement_params = statement_params + [substance]
        
        if (source != "All"):
            statement = statement + " AND `Source` = ?"
            statement_params = statement_params + [source]
        
        if (failure != "All"):
            statement = statement + " AND `FailureType` = ?"
            statement_params = statement_params + [failure]
        

        # Finish the statement with the sorting and limit parts
        statement = statement + ") ORDER BY `IncidentDate` DESC"

        cur.execute(statement, tuple(statement_params))
        rows = cur.fetchall()
        col_names = ['IncidentNumber', 'IncidentType', 'Latitude', 'Longitude',
        	'Location', 'IncidentLSD', 'IncidentSection', 'IncidentTownship',
            'IncidentRange', 'IncidentMeridian', 'LicenceNumber', 'LicenceType',
            'IncidentDate', 'IncidentNotificationDate', 'IncidentCompleteDate',
            'Source', 'CauseCategory', 'CauseType', 'FailureType', 'StrikeArea',
            'FieldCentre', 'LicenseeID', 'LicenseeName', 'InjuryCount', 
            'FatalityCount', 'Jurisdiction', 'ReleaseOffsite', 'SensitiveArea',
            'PublicAffected', 'EnvironmentAffected', 'WildlifeLivestockAffected',
            'AreaAffected', 'PublicEvacuatedCount', 'ReleaseCleanupDate',
            'PipelineLicenceSegmentID', 'PipelineLicenceLineNo', 'PipeDamageType',
            'PipeTestFailure', 'PipelineOutsideDiameter(mm)', 'PipeGrade', 
            'PipeWallThickness(mm)', 'Substance Released', 'Volume Released',
            'Volume Recovered', 'Substance Released 2', 'Volume Released 2',
            'Volume Recovered 2', 'Substance Released 3', 'Volume Released 3',
            'Volume Recovered 3', 'Substance Released 4', 'Volume Released 4',
            'Volume Recovered 4']

        def objectify(row):
            row_obj = dict(zip(col_names, row))
            return row_obj

        rows = [objectify(row) for row in rows]

        return rows
    

def lambda_handler(event, context):
    # Get all of the POST data
    location= event['Location']
    licensee = event['currentLicensee']
    substance = event['currentSubstance']
    source = event['currentSource']
    failure = event['currentFailure']
    year_min = event['yearMin']
    year_max = event['yearMax']
    volume_min = event['volumeMin']
    volume_max = event['volumeMax']
    injury_min = event['injuryMin']
    injury_max = event['injuryMax']
    fatality_min = event['fatalityMin']
    fatality_max = event['fatalityMax']

    # Fix the years to go from start of first year to end of the last.
    date_min = str(year_min) + "-01-01"
    date_max = str(year_max) + "-12-31"

    result = get_spill_info(location, date_min, date_max, volume_min, \
        volume_max, injury_min, injury_max, fatality_min, fatality_max, \
        licensee, substance, source, failure)
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True 
        },
        "body": result
    }

    # Spit out the results in json form
    return json.dumps(response)
```

Both of these lambda functions were deployed using the [lambda function deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies) functionality. Because the json and sqlite3 python libraries are standard there was no need to create virtual environments. It was as simple as uploading a zip file that contains the spills.db sqlite3 database and the python script containing the lambda function code.


#### The Web App

In addition to the changes to the backend, some minor changes have been made to the index.html and default.css code to ensure the web app works correctly with the new AWS setup. The new index.html file is:

```javascript
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="initial-scale=1.0">
        <meta charset="utf-8">
        <title>Alberta Oil and Gas Incidents 1975 - 2013</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
        <link href="default.css" rel="stylesheet">
        <!-- Google Analytics -->
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
    
      ga('create', 'UA-51737914-1', 'x10.mx');
      ga('send', 'pageview');
    
    </script>
    <!-- End Google Analytics -->
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
        <script type="text/javascript"
            src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCIxpXOSPJWNG7TnhMYq-Q2hPcM7zEQs8g&sensor=false">
        </script>
        <script>
            // Fetch the parameters from the Database to populate the filters
            var filterParameters = {};
            
            $.ajax({
                async: false,
                url : "filters.json",
                dataType : "json",
                success: function(data){
                    filterParameters = data;
                },
                error: function (data)
                {
                    alert("Couldn't retrieve the data for the filters. A page refresh will usually fix this.");
                }
            });
            
            //Make a bunch of variables to track the filters and map boundaries
            var sqlParameters = {
                currentSubstance : "All",
                currentSource : "All",
                currentLicensee : "All",
                currentFailure : "All",
                yearMin : filterParameters['dates'][0],
                yearMax : filterParameters['dates'][1],
                volumeMin : 0,
                volumeMax : filterParameters['volume'][0],
                injuryMin : 0,
                injuryMax : filterParameters['injuryCount'][0],
                fatalityMin : 0,
                fatalityMax : filterParameters['fatalityCount'][0],
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
    
            // A function to build the sliders when we are ready to do so
            function makeSliders() {
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
                            if ($(this).attr("id") == "yearBounds") {
                                sqlParameters.yearMin = ui.values[0];
                                sqlParameters.yearMax = ui.values[1];
                            } else if ($(this).attr("id") == "volume") {
                                sqlParameters.volumeMin = ui.values[0];
                                sqlParameters.volumeMax = ui.values[1];
                            } else if ($(this).attr("id") == "injuries") {
                                sqlParameters.injuryMin = ui.values[0];
                                sqlParameters.injuryMaxMax = ui.values[1];
                            } else if ($(this).attr("id") == "fatalities") {
                                sqlParameters.fatalityMin = ui.values[0];
                                sqlParameters.fatalityMax = ui.values[1];
                            }
                            getSpills();
                        }
                    });
    
                    //Initialize the text box quantity
                    var sliderlow = ("#" + $(this).attr("id") + "_amount_low");
                    $(sliderlow).val($(this).slider("values", 0));
                    
                    var sliderhigh = ("#" + $(this).attr("id") + "_amount_high");
                    $(sliderhigh).val($(this).slider("values", 1));
                
    
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
            })}
            
           
            //Accordian divs
            $(function() {
                $( "#accordion" ).accordion({   
                    collapsible: true,
                    autoHeight: false,
                    heightStyle: "content"
                });
            });
            
            //Get the Licensee list for the autocomplete widget
            var licenseeList = filterParameters['licensees'];
            
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
                $( "#substance-menu, #source-menu, #failure-menu" ).menu();
            });  
    
            //When the DOM is loaded, we want to configure stuff like the menus and sliders
            $( document ).ready(function() {
                //The menus
                makeMenus();
               
                //Set the parameters for each slider, then build them all
                $( "#yearBounds" ).data("begin", parseInt(filterParameters['dates'][0],10)); //parseInt since it hates the normal value for some reason
                $( "#yearBounds" ).data("end", parseInt(filterParameters['dates'][1],10));
                $( "#yearBounds" ).data("step", 1);
            
                $( "#volume" ).data("begin", 0);
                $( "#volume" ).data("end", parseInt(filterParameters['volume'][0]));
                $( "#volume" ).data("step", 1000);
            
                $( "#injuries" ).data("begin", 0);
                $( "#injuries" ).data("end", parseInt(filterParameters['injuryCount'][0]));
                $( "#injuries" ).data("step", 1);
            
                $( "#fatalities" ).data("begin", 0);
                $( "#fatalities" ).data("end", parseInt(filterParameters['fatalityCount'][0]));
                $( "#fatalities" ).data("step", 1);
                makeSliders();               
       
                //A hackish way to set the spill-info content max height based on window height
                document.getElementById("spill-info").style.maxHeight = $(window).height()*0.40 + "px";
                
            });
            
            
    
            //Build the menus after the window has loaded
            function makeMenus() {

                //Get the substances and sources for the filter menus
                var substanceList = filterParameters["substances"];
                //replace the initial null element
                substanceList[0] = "All";
        
                //The Sources too
                var sourceList = filterParameters['sources'];
                //replace the initial null element
                sourceList[0] = "All";
                
                //And the Failure Types
                var failureList = filterParameters['failureTypes'];
                //replace the initial null element
                failureList[0] = "All";
                
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
                constructLI("failure-links", failureList);
            }
    
            
            //Set the drop down menu to reflect the new filter value and update the displayed results
            function setText(domID, text) {
                document.getElementById(domID).innerHTML = text;
                if (domID == "substance-selected") {
                    sqlParameters.currentSubstance = text;
                } else if (domID == "source-selected") {
                    sqlParameters.currentSource = text;
                } else if (domID == "failure-selected") {
                    sqlParameters.currentFailure = text;
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
                                ATSLocation: ""
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
                    url : "https://10phigl5s2.execute-api.us-east-1.amazonaws.com/Prod/spilllocations",
                    type: "POST",
                    data : JSON.stringify(sqlParameters),
                    dataType : "json",
                    success: function(data){
                        var result = JSON.parse(data);
                        SpillLocations = result.body;  
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
                            icon: 'spotlight-poi.png',
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
                google.maps.event.addListener(marker, 'click', function() {
                    //Set the old marker back to red
                    selectedMarker.setIcon('spotlight-poi.png');
                    //Set the new marker to orange
                    selectedMarker = marker;
                    selectedMarker.setIcon('spotlight-poi-orange.png');
                    loadSpillInfo(marker.ATSLocation);
                });
            }
            
            //A function that fetches the specific spill info and loads it into the spill-info div
            function loadSpillInfo(ATSLocation) {
                
                var spillInfo = {};
                
                $.ajax({
                    async: false,
                    url : "https://10phigl5s2.execute-api.us-east-1.amazonaws.com/Prod/spillinfo",
                    type: "POST",
                    data: JSON.stringify($.extend({Location: ATSLocation}, sqlParameters)), //send ATS location + filter parameters
                    dataType : "json",
                    success: function(data){
                        var result = JSON.parse(data);
                        spillInfo = result.body;
                    },
                    error: function (data)
                    {
                        $( "#no-data" ).dialog( "open" );
                    }
                });
                
                //Clear existing content
                document.getElementById("spill-info").innerHTML = "";
                
                //A count of the selected incidents for the user to know how many spill info tables have been loaded
                var incidentCount = document.createElement('strong');
                incidentCount.innerHTML = 'Number of incidents selected: '+spillInfo.length.toString()+'<br>';
                document.getElementById("spill-info").appendChild(incidentCount);
                
                //Iterate through the JSON encoded spill info objects and create a table for each
                for (var i = 0;  i < spillInfo.length; i++){
                    var lineBreak = document.createElement('br');
                    var table = document.createElement('table');
                    
                    //Populated the new table element
                    for (var key in spillInfo[i]) {
                        if (spillInfo[i].hasOwnProperty(key)) {
                            var row = document.createElement('tr');
                            row.style.backgroundColor = "#ffebb8";
                            var cell1 = row.insertCell(0);
                            cell1.innerHTML = '<strong>'+key+'</strong>';
                            var cell2 = row.insertCell(1);
                            cell2.innerHTML = spillInfo[i][key];
                            table.appendChild(row);
                        }
                    }
                    
                    //Put the table into the div
                    document.getElementById("spill-info").appendChild(lineBreak);
                    document.getElementById("spill-info").appendChild(table);
            }
            //Open the spill info accordion section
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
                <h3>Alberta Oil and Gas Incidents 1944 - 2013</h3>
                This is a map that interactively graphs all of the recorded Oil and Gas related spills in alberta between the years 1944 and 2013. It is based on the data acquired by <a href="http://globalnews.ca/news/622513/open-data-alberta-oil-spills-1975-2013/" target="blank">Global News</a> from the <a href="http://en.wikipedia.org/wiki/Energy_Resources_Conservation_Board" target="blank">ERCB</a> (now the <a href="http://www.aer.ca/" target="blank">AER</a>).
                </br>
                </br>
                For optimal loading speeds and a clean map, it caps the number of incidents displayed to the 100 biggest spills (by volume in m<sup>3</sup>) in the current map area. Try zooming in to see more spills, or play with the provided filters to see more incidents.
                </br>
                <p>
                    Learn more about this project at:
                    <a href="/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/" target="blank">everettsprojects.com</a>
                </p>
            </div>
            <div id="accordion">
                <h3>Filter the Results</h3>
                <div id="filter-pane">
                    <p>
                        <label for="amount">Years:</label>
                        <span style="float:right;">
                            <input type="text" class="amount1" id="yearBounds_amount_low"  size="4">
                            <span class="orange-text"> - </span>  
                            <input type="text" class="amount2" id="yearBounds_amount_high" size="4">
                        </span>
                    </p>
                    <div class="slider" id="yearBounds"> </div>
            
                    <p>
                        <label for="amount">Volume:</label>
                        <span style="float:right;">
                            <input type="text" class="amount1" id="volume_amount_low" size="9">
                            <span class="orange-text"> - </span>
                            <input type="text" class="amount2" id="volume_amount_high" size="9">
                            <span class="orange-text"> m<sup>3</sup></span>
                        </span>
                    </p>
                    
                    <div class="slider" id="volume"> </div>
                    
                    <p>
                        <label for="amount">Injuries:</label>
                        <span style="float:right;">
                            <input type="text" class="amount1" id="injuries_amount_low" size="2">
                            <span class="orange-text"> - </span>
                            <input type="text" class="amount2" id="injuries_amount_high" size="2">
                        </span>
                    </p>
                    
                    <div class="slider" id="injuries"> </div>
                    
                    <p>
                        <label for="amount">Fatalities:</label>
                        <span style="float:right;">
                            <input type="text" class="amount1" id="fatalities_amount_low" size="2">
                            <span class="orange-text"> - </span>
                            <input type="text" class="amount2" id="fatalities_amount_high" size="2">
                        </span>
                    </p>
                    
                    <div class="slider" id="fatalities"> </div>
                    <br>
                    <p>
                        <div class="ui-widget">
                            <label for="licensee-selector">Company: </label>
                            <input id="licensee-selector" style="width:17em;" class="orange-text">  <span style="float:right;">[<a href=# id="licensee-clear">X</a>]</span>
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
                    <p>
                        <ul id="failure-menu">
                            <li><a href="#">Failure Type: <span id="failure-selected" class="orange-text">All</span></a>
                                <ul id="failure-links">

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
                    <a href="#" id="license-opener">Copyright (c) 2019 Everett Robinson</a> - 
            <a href="https://github.com/evjrob/Alberta-Spills-Map/">ver.3.0</a>
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
                Oops, the spill locations or data couldn't be loaded right now.
            </p>
        </div>
    </body>
</html>
```

And the new default.css is:

```css
html, body {
  background-color:#b0c4de;
  height: 100%;
  margin: 0;
  padding: 0;
  font-size: 1em;
  -webkit-text-size-adjust: none;
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
  width: 30em;
  max-height: 96%;
  position: absolute;
  font-size: 0.75em;
  top: 90px;
  left: 10px;
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

#failure-links {
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
```
