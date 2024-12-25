+++
title = "Zola-folio Theme"
description = "Moving this blog to Zola and forking my old Jekyll Theme"
date = "2024-12-24"
authors = [ "Everett Robinson",]

[taxonomies]
tags = ["Zola", "Design", "CloudFlare"]
+++

TL;DR - I created a [Zola theme](https://github.com/evjrob/zola-folio). You can use it if you'd like!

Five years ago I decided to move this blog from [Wordpress to Jekyll on AWS in an S3 Bucket](/going-serverless/). A little while later I [automated updating the blog to use a CI/CD process via AWS CodePipeline](/devops-cicd/). For insufficient reasons, I recently had the impulse to migrate this blog all over again. I have ported this blog from Jekyll to [Zola](https://www.getzola.org/) and changed hosts from AWS to CloudFlare.

Some of my reasons for this are:

1. I recently updated my laptop. I didn't feel like trying to setup a ruby environment to develop the old Jekyll blog locally.Zola is a little easier to work with. It's a single binary with no dependencies and wickedly fast by comparison.
2. The Jekyll build via AWS CodePipeline is needlessly complicated. Last time I tried to post for the first time in a while, the pipeline didn't even work. I had to trouble shoot it before my post went live!
    * The CloudFlare integration with GitHub is much simpler, and works with numerous [SPA frameworks and static site generators](https://developers.cloudflare.com/pages/framework-guides/) natively.
3. AWS nickles and dimes customers. Charging for DNS, egress out to the internet on an S3 website, plus every get or put action on items in the bucket?
    * Right off the bat, AWS charges $0.50 for a hosted zone in Route 53 to serve the bucket to a custom domain. This is most of my monthly bill.
    * This really isn't a problem for this blog. I get basically no traffic. But I never setup CloudFront for this blog, so if my traffic suddenly spiked, I could be on the hook for a big bill with AWS!
4. CloudFlare has a very attractive free tier for their Pages + Workers product, and a super easy integration with GitHub.
    * Unlimited static content serving, and 100,000 worker invocations per day? Yes please!

The first big obstacle was switching the Python lambdas I've been using for the interactive functionality on [Has the world ended yet?](https://everettsprojects.com/has-the-world-ended-yet-a-first-attempt-at-web-development/), [Mapping Oil and Gas Incidents in Alberta](https://everettsprojects.com/mapping-oil-and-gas-incidents-in-alberta-improvements/), and [A puzzling Proposal](https://everettsprojects.com/puzzling-proposal/) to use Node.js for compatibility with [CloudFlare Pages Functions](https://developers.cloudflare.com/pages/functions/). For this I just used Cursor with Claud 3.5 Sonnet. It messed up the first re-write on the [M&Ms puzzle](https://everettsprojects.com/8543W/mandms/), but fixed it straight away when I pointed out the error and intended result. I've been using Cursor and Claude a lot more when developing, and it's grown on me. I've moved from being a skeptic to a promoter of using AI for coding. These tools have come a long way from the original ChatGPT and tools like [gpt-engineer](https://github.com/gpt-engineer-org/gpt-engineer).

Another impediment to my migration was the theme. I really like the *folio theme I found on Jekyll and have been using since migrating from Wordpress. I made the somewhat crazy decision to to [fork the *folio theme to Zola](https://github.com/evjrob/zola-folio). It's a fork rather than a faithful port, because I found myself starting to fix and customize several things through the process.

In the end, none of the above are particularly great reasons to justify all the time and effort I put into the migration. I was just caught up in a desire to change things. And sometimes that's ok. It's nice to have personal space where I can make decisions that are bad from a financial or time management perspective. I feel like I learn and grow the most pursuing these little curiosities!