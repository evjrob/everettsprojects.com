+++
title = "Sharing Birb Cam Observations with the World Through iNaturalist"
description = "Integrating iNaturalist into the Birb Cam using pyinaturalist"
date = "2021-02-07"
authors = [ "Everett Robinson",]
aliases = ["/2021/02/07/sharing-birbcam-with-inaturalist.html"]

[taxonomies]
tags = ["Data Science", "Python", "Computer Vision", "Flask", "iNaturalist"]

[extra]
layout = "post"
output = "html_document"
+++

I don't appreciate the value of posting to Reddit enough. After posting the Birb Cam to the Raspberry Pi subreddit, a helpful Redditor suggested I look into posting the project's observations to iNaturalist. I had never heard of iNaturalist but decided it looked like an excellent platform. Using it to share the Birb Cam observations solves the problem of opening up all the non-critter images that might expose my neighbours' habits. It also saves me from maintaining a different version of the Birb Cam for the wide-open internet without the data labeling and revision features.

It didn't take long to discover that iNaturalist provides tools to build interaction with the platform into projects through a [REST API](https://api.inaturalist.org/v1/docs/#/). I don't even need to write the python code to interact with the REST API directly, thanks to Nicolas Noé and the other contributors to the [ipynaturalist package](https://github.com/niconoe/pyinaturalist). These tools allowed me to add the core functions and UI elements to the Birb Cam web app with very little trouble. I now provide a button to upload an observation to iNaturalist when a user opens the full-size image modal.

[![iNaturalist upload button]({{ resize_image(path="upload_button.png") }})](upload_button.png)

Clicking this button uploads the observation image and all other relevant details to [my iNaturalist account](https://www.inaturalist.org/observations?place_id=any&user_id=evjrob&verifiable=any). I indicate which images are linked with an iNaturalist observation using the iNaturalist logo. The modal icon also functions as a link to the iNaturalist observation page.

[![iNaturalist upload button]({{ resize_image(path="tooltip_inaturalist_logo.png") }})](tooltip_inaturalist_logo.png)

The Birb Cam has been an excellent pandemic project that has combined my interest in programming, machine learning, and the natural world. Integrating iNaturalist into the project was a fun development task that has kept it feeling fresh. Early on in the project's development, my sister shared a news article about how [bird watching has the same effect on happiness as a pay raise](https://www.greenmatters.com/p/birds-linked-happiness). These benefits could be real in my experience; watching the critters' antics has been something I look forward to week after week.  While working on this project is done purely for my enjoyment, I hope that sharing it on iNaturalist gives a little bit of this happiness to someone else. With that in mind, let me share one of the funniest images captured yet:

[![Squirrel fell over]({{ resize_image(path="funny_squirrel.png") }})](https://www.inaturalist.org/photos/112155844)