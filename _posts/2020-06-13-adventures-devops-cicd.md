---
title: "Adventures In DevOps: CICD Pipelines"
description: How I use AWS CodePipeline and CodeBuild to continuously deploy Visuair and this blog. Automatically update from any new commit to the master branch on GitHub!
author: "Everett Robinson"
date: "June 13, 2020"
output: html_document
layout: post
---

Last year I converted this blog to be entirely serverless. The lambda functions, associated API gateway, and public website S3 bucket were all defined by hand in the AWS console. No longer! Now a mere commit to the master branch of this blog's GitHub repository is published live within a few minutes.

