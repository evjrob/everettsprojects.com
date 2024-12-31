+++
title = "Alberta's Drilling History Visualized"
description = "An R script that plots and animates the history of oil and gas drilling activity in Alberta using ST37 data retrieved via my aertidywells R package."
date = 2017-05-22T16:39:31Z
authors = ["Everett Robinson"]
aliases = ["/2017/05/22/albertas-drilling-history-visualized/"]

[taxonomies]
tags = [ "AER", "Alberta", "Data Science", "Drilling", "Oil and Gas", "Programming", "R", "data science", "mapping",]
+++

The following animation is a map of all the Alberta Energy Regulator (AER) recorded wells drilled in Alberta between January 2010 and April of 2017:

<div style="width: 640px;">
  <!--[if lt IE 9]><![endif]--><video width="640" height="360" preload="metadata" controls="controls"><source type="video/mp4" src="wells_animation.mp4?_=1" />

  <a href="wells_animation.mp4">wells_animation.mp4</a></video>
</div>

The reduction in drilling since the latter half of 2014 due to the collapse in oil prices is clearly visible in the animation through both the histogram and the map itself. There is also a strong seasonal spike in drilling every winter. The seasonal spikes cause some challenges in comparing the true changes in the amount of drilling for different parts of the province as time goes on. I think an interesting next step will be to plot a heat map style plot of the year over year change in drilling and animate it as well. This is also just a short animation that maps only a tiny subset of Alberta’s total drilling history. Another interesting next step will be to make this code work more efficiently and to run it on a more powerful machine that can plot the entire drilling history of the province from 1883 to present.

For more detail on how this animation was created see the GitHub page for the project (<https://evjrob.github.io/AB-Drilling-History-Visualized/>) or clone the repository and experiment for yourself (<https://github.com/evjrob/AB-Drilling-History-Visualized>).

