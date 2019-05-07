---
title: "Going Serverless"
author: "Everett Robinson"
date: "April 24, 2019"
output: html_document
layout: post
---

### Why?

Back in 2017 I converted this blog from WordPress to Jekyll. It continues to run on the original web hosting I signed up for with WordPress, a service that is certainly overkill for a mostly static website. Really the only thing holding me back from moving this blog from my current provider to S3 on AWS are a few of my older projects that currently use PHP or databases on this web host.

These are:

1. [Has the world ended yet?](http://everettsprojects.com/end-of-the-world.php)
2. [Designing a secure(ish) login script with PHP and MySQL](http://everettsprojects.com/2013/02/17/designing-a-secureish-login-script-with-php-and-mysql/)
3. [Mapping Oil and Gas Incidents in Alberta with Google Maps, JQuery, and PHP](http://everettsprojects.com/2014/06/07/mapping-oil-and-gas-incidents-in-alberta-with-google-maps-jquery-and-php/)
4. [Mapping Oil and Gas Incidents in Alberta: Improvements](http://everettsprojects.com/2014/06/25/mapping-oil-and-gas-incidents-in-alberta-improvements/)


The first one is really simple. It uses PHP to check that google responds to a ping on the premise that if google is down, the world has probably ended. In 2019, it seems just as reasonable to assume that if AWS is down that the world has ended. And even if the world hasn't ended, [much of the internet probably has, at least temporarily](http://nymag.com/intelligencer/2018/03/when-amazon-web-services-goes-down-so-does-a-lot-of-the-web.html). And really that's the same thing, right?

The second is a PHP login script I decided to write while I was still an environmental science and physics undergrad. In the roughly six years since I launched it 192 accounts have been registered, five of which belong to me from initial testing. The majority of emails entered appear to be completely fake, since I never bothered to check them for validity. I really don't think it makes sense to maintain this database any longer, and no one should use my crumby PHP scripts for something so critical. I really don't like the idea of removing things from the internet, so my compromise will be to shut down the live demo, but keep the blog post and code available.

The third and fourth posts are worth keeping, and my intent is to move them to an AWS DynamoDB and lambda function setup. The usage of these pages is so low I don't expect them to cost very much at all. I'm only going to keep the improved version of the map alive, but keep the older version around as a blog post for those who are interested.

Going serverless has the potential to help me save a little money each year. By my calculations, running this little blog on AWS will cost me about \$15 per year rather than the \$60 I currently pay. This will be worth looking at more closely once I've actually built everything out and know the true costs.

### How?

As mentioned earlier, I plan to host this blog on AWS S3 going forward. Setting up an S3 bucket for this purpose is well documented, with  [official documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html) and [helpful tutorials](https://8thlight.com/blog/sarah-sunday/2018/02/14/making-a-static-website-with-jekyll-and-s3.html) to aid in the process.

The first step is to create a public S3 bucket for my blog.
