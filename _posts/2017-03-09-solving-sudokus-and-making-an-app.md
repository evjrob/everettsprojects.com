---
id: 1260
title: Solving Sudokus and Making an App
date: 2017-03-09T22:51:00+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=1260
permalink: /2017/03/09/solving-sudokus-and-making-an-app/
bento_sidebar_layout:
  - right-sidebar
bento_title_position:
  - left
bento_subtitle_color:
  - '#999999'
bento_header_image_height:
  - '10%'
bento_tile_size:
  - 1x1
bento_tile_overlay_color:
  - '#666666'
bento_tile_text_color:
  - '#ffffff'
bento_tile_text_size:
  - "16"
dsq_thread_id:
  - "6140711702"
image: https://everettsprojects.com/wp/wp-content/uploads/2017/03/SudokuBot-Solver-feature-graphic-672x372.png
categories:
  - Programming
  - Uncategorized
tags:
  - Android
  - Dancing Links
  - Go
  - Golang
  - Java
  - Knuth
  - Peter Norvig
  - puzzle
  - Simulated Annealing
  - solver
  - Sudoku
  - SudokuBot
---
My path to publishing my first app on the Google Play store has been a long one with odd beginnings. It all started when I first learned of simulated annealing algorithms from a post on [hacker news](https://news.ycombinator.com/) months ago.  In that post someone was showing off their algorithm and how it could solve the Traveling Salesman Problem or some other tough NP-Complete problem. I can&#8217;t remember the specifics, but for whatever reason it inspired me to apply the technique to another NP-Complete problem: [Sudoku puzzles!](https://github.com/evjrob/sudokuAnnealing)

I spent a couple weeks slowly working away at an implementation in Go and by the end had a configurable command line program that can reliably solve the easy puzzles, and sometimes also solve the harder ones. It doesn&#8217;t do that well on the &#8220;very hard&#8221; or &#8220;evil&#8221; Sudoku puzzles because they seem to branch early which creates excessively large peaks and troughs in the solution space that are insurmountable for my implementation. This could be because of my choice of cost function, or because I haven&#8217;t found the magic mix of parameters that maximize the likelihood of success. I incorporated some interesting tricks to the algorithm that I found while doing research; most notably the use of concurrent channels that run at exponentially increasing temperatures and thus have increasing likelihoods of escaping the deeper troughs in the search space. Each of these channels runs for a set number of iterations on their own, and then they return their current result and get compared to their neighbouring channels. Whenever a hotter channel has a better solution than a cooler channel they swap their current working solutions. The idea is that the hotter threads will keep the search from permanently getting stuck in a local minimum, while the cooler channels will inherit the best working solution and settle nicely into the minimum to find the solution if there is one.

This wasn&#8217;t the end of my Sudoku solving however. I started to wonder about deterministic algorithms for solving them and quickly stumbled onto [Peter Norvig&#8217;s Constraint Propagation Search](http://norvig.com/sudoku.html) algorithm. I set to work implementing [this algorithm in Go](https://github.com/evjrob/sudokuCps) as well, and finished it not long after. The results were far more impressive than my simulated annealing algorithm: It always got the right solution, and typically in one tenth the time on even the hardest 9 x 9 puzzles I had in my test data.

At this point my obsession with Sudoku solving algorithms was starting to peak, and I wanted to implement something even faster and more efficient than Peter Norvig&#8217;s algorithm. Eventually I stumbled onto [Donald Knuth&#8217;s Dancing Links algorithm](https://arxiv.org/abs/cs/0011047). At first I struggled to understand exactly how the algorithm worked. How could it be so much more efficient than Peter Norvig&#8217;s algorithm? It was obvious that Dancing Links avoids the computationally costly steps of copying the entire puzzle when a branch in the search space occurs, but I was still having trouble understanding how exactly it managed to backtrack and reverse the changes it made without copying. And so I spent far too much time [drawing up the example problem in his paper](https://github.com/evjrob/dancing-links-visualized) using a flow charting web app.

<div id='gallery-1' class='gallery galleryid-1260 gallery-columns-1 gallery-size-large'>
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/0-Dancing-Links-Start.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/0-Dancing-Links-Start.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1261" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/0-Dancing-Links-Start.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/0-Dancing-Links-Start-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1261'>
      0 &#8211; Dancing Links Start
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/1-SearchA-CoverA.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/1-SearchA-CoverA.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1262" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/1-SearchA-CoverA.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/1-SearchA-CoverA-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1262'>
      1 &#8211; Search(A) &#8211; Cover(A)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/2-SearchA-CoverD.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/2-SearchA-CoverD.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1263" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/2-SearchA-CoverD.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/2-SearchA-CoverD-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1263'>
      2 &#8211; Search(A) &#8211; Cover(D)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/3-SearchA-CoverG.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/3-SearchA-CoverG.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1264" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/3-SearchA-CoverG.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/3-SearchA-CoverG-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1264'>
      3 &#8211; Search(A) &#8211; Cover(G)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/4-SearchB-CoverB.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/4-SearchB-CoverB.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1265" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/4-SearchB-CoverB.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/4-SearchB-CoverB-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1265'>
      4 &#8211; Search(B) &#8211; Cover(B)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/5-SearchB-CoverC.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/5-SearchB-CoverC.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1266" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/5-SearchB-CoverC.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/5-SearchB-CoverC-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1266'>
      5 &#8211; Search(B) &#8211; Cover(C)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/6-SearchB-CoverF.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/6-SearchB-CoverF.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1267" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/6-SearchB-CoverF.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/6-SearchB-CoverF-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1267'>
      6 &#8211; Search(B) &#8211; Cover(F)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/7-SearchE-CoverE.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/7-SearchE-CoverE.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1268" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/7-SearchE-CoverE.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/7-SearchE-CoverE-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1268'>
      7 &#8211; Search(E) &#8211; Cover(E)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/8-SearchB-UncoverF.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/8-SearchB-UncoverF.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1269" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/8-SearchB-UncoverF.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/8-SearchB-UncoverF-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1269'>
      8 &#8211; Search(B) &#8211; Uncover(F)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/9-SearchB-UncoverC.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/9-SearchB-UncoverC.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1270" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/9-SearchB-UncoverC.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/9-SearchB-UncoverC-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1270'>
      9 &#8211; Search(B) &#8211; Uncover(C)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/10-SearchB-UncoverB.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/10-SearchB-UncoverB.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1271" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/10-SearchB-UncoverB.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/10-SearchB-UncoverB-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1271'>
      10 &#8211; Search(B) &#8211; Uncover(B)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/11-SearchA-UncoverG.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/11-SearchA-UncoverG.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1272" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/11-SearchA-UncoverG.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/11-SearchA-UncoverG-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1272'>
      11 &#8211; Search(A) &#8211; Uncover(G)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/12-SearchA-UncoverD.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/12-SearchA-UncoverD.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1273" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/12-SearchA-UncoverD.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/12-SearchA-UncoverD-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1273'>
      12 &#8211; Search(A) &#8211; Uncover(D)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/13-SearchA-CoverD.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/13-SearchA-CoverD.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1274" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/13-SearchA-CoverD.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/13-SearchA-CoverD-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1274'>
      13 &#8211; Search(A) &#8211; Cover(D)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/14-SearchB-CoverB.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/14-SearchB-CoverB.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1275" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/14-SearchB-CoverB.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/14-SearchB-CoverB-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1275'>
      14 &#8211; Search(B) &#8211; Cover(B)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/15-SearchB-CoverC.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/15-SearchB-CoverC.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1276" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/15-SearchB-CoverC.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/15-SearchB-CoverC-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1276'>
      15 &#8211; Search(B) &#8211; Cover(C)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/16-SearchB-CoverF.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/16-SearchB-CoverF.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1277" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/16-SearchB-CoverF.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/16-SearchB-CoverF-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1277'>
      16 &#8211; Search(B) &#8211; Cover(F)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/17-SearchB-CoverG.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/17-SearchB-CoverG.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1278" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/17-SearchB-CoverG.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/17-SearchB-CoverG-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1278'>
      17 &#8211; Search(B) &#8211; Cover(G)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/18-SearchE-CoverE.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/18-SearchE-CoverE.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1279" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/18-SearchE-CoverE.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/18-SearchE-CoverE-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1279'>
      18 &#8211; Search(E) &#8211; Cover(E)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/19-SearchB-UncoverG.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/19-SearchB-UncoverG.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1280" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/19-SearchB-UncoverG.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/19-SearchB-UncoverG-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1280'>
      19 &#8211; Search(B) &#8211; Uncover(G)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/20-SearchB-UncoverF.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/20-SearchB-UncoverF.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1281" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/20-SearchB-UncoverF.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/20-SearchB-UncoverF-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1281'>
      20 &#8211; Search(B) &#8211; Uncover(F)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/21-SearchB-UncoverC.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/21-SearchB-UncoverC.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1282" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/21-SearchB-UncoverC.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/21-SearchB-UncoverC-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1282'>
      21 &#8211; Search(B) &#8211; Uncover(C)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/22-SearchB-CoverG.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/22-SearchB-CoverG.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1283" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/22-SearchB-CoverG.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/22-SearchB-CoverG-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1283'>
      22 &#8211; Search(B) &#8211; Cover(G)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/23-SearchC-CoverC.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/23-SearchC-CoverC.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1284" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/23-SearchC-CoverC.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/23-SearchC-CoverC-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1284'>
      23 &#8211; Search(C) &#8211; Cover(C)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/24-SearchC-CoverE.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/24-SearchC-CoverE.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1285" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/24-SearchC-CoverE.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/24-SearchC-CoverE-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1285'>
      24 &#8211; Search(C) &#8211; Cover(E)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/25-SearchC-CoverF.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/25-SearchC-CoverF.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1286" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/25-SearchC-CoverF.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/25-SearchC-CoverF-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1286'>
      25 &#8211; Search(C) &#8211; Cover(F)
    </dd>
  </dl>
  
  <br style="clear: both" />
  
  <dl class='gallery-item'>
    <dt class='gallery-icon landscape'>
      <a href='https://everettsprojects.com/wp/wp-content/uploads/2017/03/26-Searchh-Return.png'><img width="701" height="661" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/26-Searchh-Return.png" class="attachment-large size-large" alt="" aria-describedby="gallery-1-1287" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/26-Searchh-Return.png 701w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/26-Searchh-Return-300x283.png 300w" sizes="(max-width: 701px) 100vw, 701px" /></a>
    </dt>
    
    <dd class='wp-caption-text gallery-caption' id='gallery-1-1287'>
      26 &#8211; Search(h) &#8211; Return
    </dd>
  </dl>
  
  <br style="clear: both" />
</div>

Finally I understood it. I saw the dance occur right before my eyes, and no longer felt unworthy of applying it to my sudokus. And so I created [another Go package called sudokuDlx.](https://github.com/evjrob/sudokuDlx) It manages to solve my sudoku puzzles much faster than the Constraint Propagation Search algorithm; it solves the full set of about 150 test puzzles in about half a second on my laptop versus more than 16 seconds for sudokuCPS. This advantage of speed is most noticeable when we attempt to solve Peter Norvig&#8217;s impossible puzzle. Here sudokuDlx determines the puzzle is impossible almost as fast as it takes to solve any valid puzzle while sudokuCPS takes an agonizing 10 minutes and 52 seconds to do the same task.

Having finished the Dancing Links implementation, I put the whole business of solving sudokus on hold. I spent most of the ensuing time on [Udacity learning how to develop an android app](https://www.udacity.com/course/new-android-fundamentals--ud851). I sort of imagined trying to find some application for my new found sudoku solving skills when I started learning android development, but a major problem existed: Most android programs are written in Java, while all of my sudoku solvers are written in Go. I knew it would be possible to re-write the algorithms in Java, but I wasn&#8217;t super enthused about having to do that. I was almost prepared to find some other project to make into an android app, but decided to investigate [Gomobile](https://godoc.org/golang.org/x/mobile/cmd/gomobile) a little bit before giving up. It has quite a few limitations about the types and data structures that can be passed from Java to go and vice versa, but nothing that a few wrapper functions in the GO package can&#8217;t handle.

I set to work making my sudoku solving android app and after a couple dozen hours of development spread over evenings and weekends I finally have an app I feel is worth publishing. The code for this app is up on [GitHub](https://github.com/evjrob/SudokuBotSolver) and the app itself can be downloaded on the [Google Play store](https://play.google.com/store/apps/details?id=com.everettsprojects.sudokubotsolver&hl=en).

<div id='gallery-2' class='gallery galleryid-1260 gallery-columns-2 gallery-size-large'>
  <dl class='gallery-item'>
    <dt class='gallery-icon portrait'>
      <a href='http://everettsprojects.com/2017/03/09/solving-sudokus-and-making-an-app/screenshot_20170308-204149/'><img width="576" height="1024" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204149-576x1024.png" class="attachment-large size-large" alt="" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204149-576x1024.png 576w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204149-146x260.png 146w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204149-768x1365.png 768w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204149.png 1080w" sizes="(max-width: 576px) 100vw, 576px" /></a>
    </dt>
  </dl>
  
  <dl class='gallery-item'>
    <dt class='gallery-icon portrait'>
      <a href='http://everettsprojects.com/2017/03/09/solving-sudokus-and-making-an-app/screenshot_20170308-204203/'><img width="576" height="1024" src="https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204203-576x1024.png" class="attachment-large size-large" alt="" srcset="https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204203-576x1024.png 576w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204203-146x260.png 146w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204203-768x1365.png 768w, https://everettsprojects.com/wp/wp-content/uploads/2017/03/Screenshot_20170308-204203.png 1080w" sizes="(max-width: 576px) 100vw, 576px" /></a>
    </dt>
  </dl>
  
  <br style="clear: both" />
</div>