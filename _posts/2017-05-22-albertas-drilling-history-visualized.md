---
id: 1317
title: "Alberta's Drilling History Visualized"
date: 2017-05-22T16:39:31+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=1317
permalink: /2017/05/22/albertas-drilling-history-visualized/
bento_sidebar_layout:
  - right-sidebar
bento_title_position:
  - left
bento_subtitle_color:
  - '#999999'
bento_header_image_height:
  - '10%'
bento_header_overlay_opacity:
  - "0"
bento_tile_size:
  - 1x1
bento_tile_overlay_color:
  - '#666666'
bento_tile_overlay_opacity:
  - "0"
bento_tile_text_color:
  - '#ffffff'
bento_tile_text_size:
  - "16"
enclosure:
  - |
    https://everettsprojects.com/wp/wp-content/uploads/2017/05/wells_animation.mp4
    645343
    video/mp4

dsq_thread_id:
  - "6141306913"
categories:
  - Data Science
  - Programming
tags:
  - AER
  - Alberta
  - data science
  - Drilling
  - mapping
  - Oil and Gas
  - R
---
The following animation is a map of all the Alberta Energy Regulator (AER) recorded wells drilled in Alberta between January 2010 and April of 2017:

<div style="width: 640px;" class="wp-video">
  <!--[if lt IE 9]><![endif]--><video class="wp-video-shortcode" id="video-1317-1" width="640" height="360" preload="metadata" controls="controls"><source type="video/mp4" src="https://everettsprojects.com/wp/wp-content/uploads/2017/05/wells_animation.mp4?_=1" />

  <a href="https://everettsprojects.com/wp/wp-content/uploads/2017/05/wells_animation.mp4">https://everettsprojects.com/wp/wp-content/uploads/2017/05/wells_animation.mp4</a></video>
</div>

The reduction in drilling since the latter half of 2014 due to the collapse in oil prices is clearly visible in the animation through both the histogram and the map itself. There is also a strong seasonal spike in drilling every winter. The seasonal spikes cause some challenges in comparing the true changes in the amount of drilling for different parts of the province as time goes on. I think an interesting next step will be to plot a heat map style plot of the year over year change in drilling and animate it as well. This is also just a short animation that maps only a tiny subset of Alberta’s total drilling history. Another interesting next step will be to make this code work more efficiently and to run it on a more powerful machine that can plot the entire drilling history of the province from 1883 to present.

For more detail on how this animation was created see the GitHub page for the project (<https://evjrob.github.io/AB-Drilling-History-Visualized/>) or clone the repository and experiment for yourself (<https://github.com/evjrob/AB-Drilling-History-Visualized>).

&nbsp;

&nbsp;

&nbsp;
