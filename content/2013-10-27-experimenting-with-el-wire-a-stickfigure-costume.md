+++
title = "Experimenting with EL wire: A Stickfigure Costume"
description = "Maker project - Home made Halloween stick figure costume using EL wire"
date = 2013-10-27T19:42:11Z
authors = ["Everett Robinson"]
aliases = ["/2013/10/27/experimenting-with-el-wire-a-stickfigure-costume/"]

[taxonomies]
tags = [ "Adafruit", "Costume", "DIY", "E-textiles", "EL wire", "Electronics", "Halloween", "Soldering",]

[extra]
layout = "post"
id = 853
permalink = "/2013/10/27/experimenting-with-el-wire-a-stickfigure-costume/"
geo_latitude = [ "0.000000",]
geo_longitude = [ "0.000000",]
geo_accuracy = [ "0",]
geo_public = [ "1",]
image = "/wp-content/uploads/2013/10/img_2396-672x372.jpg"
comments = true
+++

[<img class="aligncenter size-full wp-image-877" alt="IMG_2396" src="/wp-content/uploads/2013/10/img_2396.jpg" width="594" height="445" srcset="/wp-content/uploads/2013/10/img_2396.jpg 4608w, /wp-content/uploads/2013/10/img_2396-300x225.jpg 300w, /wp-content/uploads/2013/10/img_2396-1024x768.jpg 1024w" sizes="(max-width: 594px) 100vw, 594px" />](/wp-content/uploads/2013/10/img_2396.jpg)

Like most people on the internet, I saw [this video](http://www.youtube.com/watch?v=GkBDRUO8hAo) leading up to this year&#8217;s Halloween. Unlike most people, I thought &#8220;I need to make one of those, but adult male sized!&#8221; A quick bit of research led me to realize that normal LED light strips as used in the video are a little impractical for a suit my size. They cost more than 4x as much per unit length compared to High brightness EL Wire and they appear to consume far more power as well. Not wanting to carry piles of spare batteries around when I go out for Halloween, I decided to use EL wire and settle for the few tradeoffs it has. The most major tradeoff is that EL wire doesn&#8217;t hold up as well to repeated flex in the joints or tight bends. I may regret the choice to use EL wire if it fails on the dance floor, but for now it seems like the smarter choice.

<p style="text-align:center;">
  . . . . .
</p>

<p style="text-align:left;"></p>
### The Parts:

  * 2 x  [2.5m of High Brightness White Electroluminescent (EL) Wire](http://www.adafruit.com/products/410)
  * 1 x [12V EL wire/tape inverter](http://www.adafruit.com/products/448)
  * 1 x [In-line wire 1-to-4 splitter](http://www.adafruit.com/products/402)
  * 1 x [In-line power cable 1 meter long extension cord](http://www.adafruit.com/products/616)
  * 1 x [In-line power wire connector (female)](http://www.adafruit.com/products/318)
  * 3 x[ In-line power wire connector (male)](http://www.adafruit.com/products/319)
  * 1 x [Copper Foil Tape with Conductive Adhesive &#8211; 6mm x 15 meter roll](http://www.adafruit.com/products/1128)
  * 1 x [Heat Shrink Pack](http://www.adafruit.com/products/344)

<p>
  <a href="/wp-content/uploads/2013/10/img_23691.jpg"><img class="aligncenter  wp-image-885" alt="IMG_2369" src="/wp-content/uploads/2013/10/img_23691.jpg" width="356" height="267" srcset="/wp-content/uploads/2013/10/img_23691.jpg 2304w, /wp-content/uploads/2013/10/img_23691-300x225.jpg 300w, /wp-content/uploads/2013/10/img_23691-1024x768.jpg 1024w" sizes="(max-width: 356px) 100vw, 356px" /></a>
</p>

<p style="text-align:center;">
  . . . . .
</p>

### The Basic Design:

[<img class="aligncenter size-full wp-image-869" alt="SuitLayout" src="/wp-content/uploads/2013/10/suitlayout.jpg" width="594" height="655" srcset="/wp-content/uploads/2013/10/suitlayout.jpg 2338w, /wp-content/uploads/2013/10/suitlayout-271x300.jpg 271w, /wp-content/uploads/2013/10/suitlayout-928x1024.jpg 928w" sizes="(max-width: 594px) 100vw, 594px" />](/wp-content/uploads/2013/10/suitlayout.jpg)

The suit consists of five separate strands of EL wire of varying lengths all connected to the inverter and power source. The hood of the suit is held into a circular shape using an aluminium ring that was salvaged from an old tomato cage. The inverter and battery pack is crammed into a small reusable container that has been cut up and modified to house the components.

[<img class="aligncenter size-full wp-image-868" alt="ElectronicsBox" src="/wp-content/uploads/2013/10/electronicsbox.jpg" width="594" height="356" srcset="/wp-content/uploads/2013/10/electronicsbox.jpg 1784w, /wp-content/uploads/2013/10/electronicsbox-300x180.jpg 300w, /wp-content/uploads/2013/10/electronicsbox-1024x614.jpg 1024w" sizes="(max-width: 594px) 100vw, 594px" />](/wp-content/uploads/2013/10/electronicsbox.jpg)

<p style="text-align:center;">
  . . . . .
</p>

<p style="text-align:left;"></p>
### Preparing the Electronics:

The strands of EL wire that I purchased both come with jumpers preinstalled, but since I needed five separate strands it was necessary to cut off the extra strands from the ends and manually solder new connections to them. There were three of these new strands to be soldered using the male in-line connectors. A few images of my soldering efforts are included, but the [adafruit guide to soldering EL wire](http://learn.adafruit.com/el-wire/soldering-to-el-wire) is far superior to anything I could reproduce here.

<table>
  <tr>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2387.jpg"><img class="wp-image-898 alignnone" alt="IMG_2387" src="/wp-content/uploads/2013/10/img_2387.jpg" width="257" height="193" /></a>
    </td>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2390.jpg"><img class="wp-image-899 alignnone" alt="IMG_2390" src="/wp-content/uploads/2013/10/img_2390.jpg" width="257" height="193" /></a>
    </td>
  </tr>
</table>

<p style="text-align:left;">
  After cutting the EL wire to size and soldering on the jumpers it was time to prepare some of the other wiring essentials, like a Y shaped extension cable for the arms. This was done by simply cutting the female end of the in-line extension cord off, and then resoldering it with a the second female connector attached. The junction was then sealed up tight with a little heat shrink tubing that I slid on before I soldered everything.
</p>

<p>
  <a href="/wp-content/uploads/2013/10/img_2391.jpg"><img class="aligncenter  wp-image-900" alt="IMG_2391" src="/wp-content/uploads/2013/10/img_2391.jpg" width="356" height="267" /></a>
</p>

<p style="text-align:left;">
  And finally, as far as the electronics are concerned, all that needs to be done is assemble the power supply and inverter box. The box, contrary to my measurements, unfortunately didn&#8217;t quite fit the battery pack and inverter. To fix this I decided to modify the box with a little lighter and X-acto knife surgery.  After that, it was necessary to drill a hole for the toggle switch I planned to install. Technically I drilled the hole in the wrong place originally, and had to drill a second one. It&#8217;s not a mistake, just ventilation!
</p>

<table>
  <tr>
    <td>
      <a href="/wp-content/uploads/2013/10/img_23721.jpg"><img class="wp-image-887 alignnone" alt="IMG_2372" src="/wp-content/uploads/2013/10/img_23721.jpg" width="247" height="185" srcset="/wp-content/uploads/2013/10/img_23721.jpg 2304w, /wp-content/uploads/2013/10/img_23721-300x225.jpg 300w, /wp-content/uploads/2013/10/img_23721-1024x768.jpg 1024w" sizes="(max-width: 247px) 100vw, 247px" /></a>
    </td>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2373.jpg"><img class="wp-image-888 alignnone" alt="IMG_2373" src="/wp-content/uploads/2013/10/img_2373.jpg" width="247" height="185" srcset="/wp-content/uploads/2013/10/img_2373.jpg 2304w, /wp-content/uploads/2013/10/img_2373-300x225.jpg 300w, /wp-content/uploads/2013/10/img_2373-1024x768.jpg 1024w" sizes="(max-width: 247px) 100vw, 247px" /></a>
    </td>
  </tr>
</table>

<p style="text-align:left;">
  After getting the box ready to house the electronics, it was time to get soldering again. The connections are all really simple, I just soldered the two black leads together and then protected the joint with some more heat shrink tubing. After that the red leads were connected to the two terminals of the toggle switch I harvested from something too long ago to remember what it was. Once again, the connections were wrapped up tight with heat shrink tubing and then for good measure I placed a small bead of hot glue between them.
</p>

<p>
  <a href="/wp-content/uploads/2013/10/img_2382.jpg"><img class="aligncenter  wp-image-894" alt="IMG_2382" src="/wp-content/uploads/2013/10/img_2382.jpg" width="356" height="267" /></a>
</p>

<p style="text-align:left;">
  With the soldering done, I just had to fit it all into my box. This was really just as simple as screwing the nut onto the threaded bit of the toggle switch after sticking it through the hole that I had drilled, then squeezing the battery pack and inverter into there. Everything fits so snug that I didn&#8217;t need to do any fastening of the components to the inside of the box. Lucky me.
</p>

<table>
  <tr>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2375.jpg"><img class="wp-image-890" alt="IMG_2375" src="/wp-content/uploads/2013/10/img_2375.jpg" width="249" height="187" /></a>
    </td>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2383.jpg"><img class="wp-image-895 alignnone" alt="IMG_2383" src="/wp-content/uploads/2013/10/img_2383.jpg" width="249" height="187" /></a>
    </td>
  </tr>
</table>

<p style="text-align:center;">
  . . . . .
</p>

<p style="text-align:left;"></p>
### Attaching it to the Clothes:

<p style="text-align:left;">
  Okay so the electronics are done, and everything glows nicely. Now we jut need to sew it to the clothing. But before that, I decided I wanted a nice round stick person head. To achieve this I went and pulled a nice firm aluminium  ring from an old tomato cage then stuck it through the drawstring part of the hood.
</p>

<table>
  <tr>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2384.jpg"><img class="wp-image-896 alignnone" alt="IMG_2384" src="/wp-content/uploads/2013/10/img_2384.jpg" width="249" height="187" /></a>
    </td>
    <td>
      <a href="/wp-content/uploads/2013/10/img_2385.jpg"><img class="wp-image-897 alignnone" alt="IMG_2385" src="/wp-content/uploads/2013/10/img_2385.jpg" width="249" height="187" /></a>
    </td>
  </tr>
</table>

<p style="text-align:left;">
  To sew the EL wire on I used transparent thread, but that&#8217;s really just a fancy marketing gimmick used to sell 6 lb fishing line to the sewing demographic. I used a very simple rib stitch that wrapped around the EL wire then through the fabric over and over again. After this was done I decided to ensure the EL wire stayed put by further tacking it on using a few blobs of strategically placed hot glue. It&#8217;s okay, no one will notice in the dark.
</p>

<p style="text-align:left;">
  I then started to sew on one of the arms, but due to my generally incompetent sewing skills, it failed to hold the EL wire in place after repeated movement. A little fed up, I resorted to the hot glue gun again. By putting little beads in places where the EL wire wasn&#8217;t moving too much and leaving high movement areas like the joints free I managed to get a solution that holds the EL wire onto the clothing well while still maintaining a good degree of freedom of movement. I repeated this process for the other arm and both legs, with the added benefit that it is much faster than sewing.
</p>

<p>
  <a href="/wp-content/uploads/2013/10/img_2394.jpg"><img class="aligncenter  wp-image-901" alt="IMG_2394" src="/wp-content/uploads/2013/10/img_2394.jpg" width="356" height="267" /></a>
</p>

<p style="text-align:left;">
  All that remained to be done at this point is to hook up the EL wire to the power box. This is where the 1 to 4 splitter comes in handy to connect to the torso/head, two legs, and the Y extension to the arms. All of this wiring is hidden inside the hoodie and threaded through a hole on the inside of the front pouch pocket where I&#8217;ve hidden the power box.  That&#8217;s really all there is to it, and the costume is ready to go for Halloween.
</p>

<p style="text-align:left;">
  <a href="/wp-content/uploads/2013/10/img_2395.jpg"><img class="aligncenter size-full wp-image-902" alt="IMG_2395" src="/wp-content/uploads/2013/10/img_2395.jpg" width="594" height="445" /></a>
</p>
