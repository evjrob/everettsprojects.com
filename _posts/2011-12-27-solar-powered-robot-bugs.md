---
id: 74
title: Solar Powered Robot Bugs!
description: 'A microcontroller free solar powered autonomous robot based on BEAM robotics principles. Robotics kit sold by Solarbotics Ltd.'
date: 2011-12-27T02:03:12+00:00
author: Everett
layout: post
guid: http://ejrob.wordpress.com/?p=74
permalink: /2011/12/27/solar-powered-robot-bugs/
twitter_cards_summary_img_size:
  - 'a:7:{i:0;i:2565;i:1;i:1927;i:2;i:2;i:3;s:26:"width="2565" height="1927"";s:4:"bits";i:8;s:8:"channels";i:3;s:4:"mime";s:10:"image/jpeg";}'
image: /wp-content/uploads/2011/12/dscf27821-672x372.jpg
categories:
  - Electronics
  - Kits
  - Robotics
tags:
  - Solarbotics
comments: true
---
<div id="attachment_92" style="width: 600px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2011/12/dscf2781.jpg"><img class="wp-image-92 " title="DSCF2781" src="/wp-content/uploads/2011/12/dscf2781.jpg" alt="The finished photopopper photovore" width="590" height="445" /></a>

  <p class="wp-caption-text">
    The finished product
  </p>
</div>

<div id="attachment_84" style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2011/12/dscf2751.jpg"><img class="wp-image-84 " title="DSCF2751" src="/wp-content/uploads/2011/12/dscf2751.jpg" alt="My new Hakko FX-888 soldering station" width="300" height="252" srcset="/wp-content/uploads/2011/12/dscf2751.jpg 2591w, /wp-content/uploads/2011/12/dscf2751-300x252.jpg 300w, /wp-content/uploads/2011/12/dscf2751-1024x863.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    My new Hakko FX-888 soldering station
  </p>
</div>

<p style="text-align: left;">
  This is not a project in which I spent much time designing or planning things myself, but I had a lot of fun with it, and it let me try out my brand new Hakko soldering station. It simply entails the assembly of the <a href="http://www.solarbotics.com/products/k_pp/">Photopopper Photovore robot kit</a> from <a href="http://www.solarbotics.com">Solarbotics.com</a> . What is a Photopopper Photovore? It&#8217;s basically a small solar powered robot, which uses Infrared and tactile sensors to simultaneously move towards sources of light and avoid obstacles. It also bears resemblance to an insect, especially a stinkbug. This kit really interests me, because the &#8220;behaviour&#8221; of the robot is caused through hardwired circuitry alone, and no microcontrollers or code are needed. The description included by Solarbotics says it is based on something called MillerEngine technology which (in all honesty) means nothing to me. Regardless, the circuit isn&#8217;t overly difficult to follow, and one need not know what a MillerEngine is to appreciate it.
</p>

<div id="attachment_110" style="width: 599px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2011/12/photopoppercircuit.png"><img class=" wp-image-110    " title="PhotopopperCircuit" src="/wp-content/uploads/2011/12/photopoppercircuit.png" alt="The Photopopper Photovore circuit" width="589" height="260" srcset="/wp-content/uploads/2011/12/photopoppercircuit.png 1011w, /wp-content/uploads/2011/12/photopoppercircuit-300x132.png 300w" sizes="(max-width: 589px) 100vw, 589px" /></a>

  <p class="wp-caption-text">
    The Photopopper Photovore circuit
  </p>
</div>

Since I am only a hobbyist, my assessment may not be correct, but hopefully I&#8217;m not too far off the mark. Essentially what happens is that the solar cell charges the large 4.7mF capacitor (C1), and then when the voltage in the capacitor is high enough, the voltage trigger on one of the sides engages.The determination of which voltage trigger is engaged is determined by the IR and tactile sensors, where the tactile sensors take priority over the IR sensors to ensure obstacle avoidance in addition to the light seeking behaviour. The voltage trigger then trips the corresponding transistor which applies a current across the motor on that side until the voltage  drops enough to disengage the voltage trigger. The small capacitors (C2 and C3) are responsible for determining the length and frequency of the motor activity by affecting the voltage at the voltage triggers, and the diodes simply make sure the current moves in the correct direction. The trimpot makes it possible to tune the robot to favor one side over the other, or to balance it so that it moves directly towards sources of light.

Before going further, I feel like it would be a good idea to make it clear that this project was very enjoyable even though I encountered several issues while working on it. I wouldn&#8217;t want to discourage anyone from taking it on simply because I like to complain about things.

<div id="attachment_83" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2011/12/dscf2749.jpg"><img class="size-medium wp-image-83  " title="DSCF2749" src="/wp-content/uploads/2011/12/dscf2749.jpg?w=300" alt="The components all laid out" width="300" height="225" srcset="/wp-content/uploads/2011/12/dscf2749.jpg 3664w, /wp-content/uploads/2011/12/dscf2749-300x225.jpg 300w, /wp-content/uploads/2011/12/dscf2749-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The components all laid out (I apologize for the blurriness)
  </p>
</div>

The assembly instructions were good, and I really can&#8217;t complain too much in that regard. To start, you are shown a parts list, so you can be sure you have all the necessary components before proceeding. The most interesting part in this kit is probably the PCB, which is cut and formed to make this robot recognizable as an insect. In addition, there is  a large capacitor, trimpot, solar cell, and a pair each of diodes, voltage triggers, transistors, capacitors, motors, IR sensors, and the components to make each antenna (the tactile sensors).

<div id="attachment_87" style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2011/12/dscf2764.jpg"><img class="size-medium wp-image-87 " title="DSCF2764" src="/wp-content/uploads/2011/12/dscf2764.jpg?w=300" alt="The underside of the PCB" width="300" height="219" srcset="/wp-content/uploads/2011/12/dscf2764.jpg 1833w, /wp-content/uploads/2011/12/dscf2764-300x219.jpg 300w, /wp-content/uploads/2011/12/dscf2764-1024x750.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The underside with the voltage triggers, diodes, transistors, capacitors and trimpot installed
  </p>
</div>

The first components to be installed are the voltage triggers, trimpot, and diodes, followed by the transistors and small capacitors. After this, the IR sensors are added. The installation of all these components was fairly straight forward, and was easily accomplished with the new soldering iron.

<div id="attachment_88" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2011/12/dscf2771.jpg"><img class="size-medium wp-image-88" title="DSCF2771" src="/wp-content/uploads/2011/12/dscf2771.jpg?w=300" alt="The motor mounts with motors soldered on" width="300" height="225" srcset="/wp-content/uploads/2011/12/dscf2771.jpg 2565w, /wp-content/uploads/2011/12/dscf2771-300x225.jpg 300w, /wp-content/uploads/2011/12/dscf2771-1024x769.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The motor mounts with motors soldered on
  </p>
</div>

The next component to go on was the large storage capacitor, which had to have its leads bent 90 degrees so that it could lie flat against the PCB. The motor mounts were also fairly easy to attach, using a combination of folding tabs and plenty of solder. Once attached, the motors themselves simply clipped into place.

<div id="attachment_91" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2011/12/dscf2780.jpg"><img class="size-medium wp-image-91" title="DSCF2780" src="/wp-content/uploads/2011/12/dscf2780.jpg?w=300" alt="The support wire" width="300" height="239" srcset="/wp-content/uploads/2011/12/dscf2780.jpg 2187w, /wp-content/uploads/2011/12/dscf2780-300x239.jpg 300w, /wp-content/uploads/2011/12/dscf2780-1024x817.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The support wire: Murphy&#8217;s Law finally shows up.
  </p>
</div>

Next, it was necessary to install the support wire to ensure the photopopper&#8217;s legs would reach the ground. Unfortunately this is where my problems began, since I failed to make sure the wire was short enough before I began soldering it on. While it is technically possible to fix this by twisting it to increase tension, I found the spring of the PCB itself was stronger than the wire and I had to constantly re-tighten it. Eventually metal fatigue occurred, and the poor wire broke. Luckily I had a paperclip of a similar gauge (seen in the picture to the left) which seemed to be much stronger, and was capable of withstanding the flex of the PCB. After this, some of the heat-shrink tubing was applied to the motor shafts to make the tires/feet, and the paperclip was given a small twist to make sure they reached the ground.

<div id="attachment_90" style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2011/12/dscf2777.jpg"><img class="size-medium wp-image-90" title="DSCF2777" src="/wp-content/uploads/2011/12/dscf2777.jpg?w=300" alt="The solar panel is now attached" width="300" height="215" srcset="/wp-content/uploads/2011/12/dscf2777.jpg 1909w, /wp-content/uploads/2011/12/dscf2777-300x215.jpg 300w, /wp-content/uploads/2011/12/dscf2777-1024x734.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The solar panel is now attached
  </p>
</div>

Attaching the solar cell was fairly easy, though wire strippers were needed to prepare the twisted red and black wire before it could be soldered to the right places. A piece of double sided sticky tape was then used to hold it into place. This was the next source of problems, because I mounted the solar panel before making sure each of the motors was working, and ruined it when I removed the panel to resolder one of the wires to the board. Luckily I had a replacement available, and I tested the conductivity of the adhesive before use to make sure it would not short anything. To best way to test each motor is to place the robot in direct sunlight or under an incandescent lightbulb, and then use something to short the square and circle pads on each side of the robot&#8217;s head (where the antennae will later be installed). From experience I recommend this step is performed before the solar panel is mounted. It is now a good idea to tune to robot, before the antenna are installed. To achieve this, the robot should be put near a source of light, and then the trimpot should be adjusted to make sure it moves towards that source, and doesn&#8217;t veer to either side. after this is achieved it is best to not to fiddle with it, as troubleshooting antennae and IR sensor balance at the same time was unnecessarily difficult.

<div id="attachment_148" style="width: 604px" class="wp-caption aligncenter">
  <a href="/wp-content/uploads/2011/12/antennae.png"><img class="size-full wp-image-148" title="Antennae" src="/wp-content/uploads/2011/12/antennae.png" alt="The structure of the tactile sensors" width="594" height="298" srcset="/wp-content/uploads/2011/12/antennae.png 875w, /wp-content/uploads/2011/12/antennae-300x150.png 300w" sizes="(max-width: 594px) 100vw, 594px" /></a>

  <p class="wp-caption-text">
    The structure of the tactile sensors
  </p>
</div>

<div id="attachment_93" style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2011/12/dscf27821.jpg"><img class=" wp-image-93" title="DSCF2782" src="/wp-content/uploads/2011/12/dscf27821.jpg?w=300" alt="Antennae installed" width="300" height="225" srcset="/wp-content/uploads/2011/12/dscf27821.jpg 2564w, /wp-content/uploads/2011/12/dscf27821-300x225.jpg 300w, /wp-content/uploads/2011/12/dscf27821-1024x769.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    With the antennae installed
  </p>
</div>

The idea behind the tactile sensors is that when they collide with something it causes the spring to bend and connect with the central pin. This shorts the circuit and bypasses the IR sensor to make sure the robot moves away from obstacles. This step was especially troublesome, since the heat shrink tubing didn&#8217;t contract enough, and the spring would not fit without significant forcing. Through a combination of slightly untwisting the spring to increase its diameter, forcing the tubing through with a screwdriver, and applying excessive force (enough to bend the pin), the spring was eventually moved into place. The antennae were then ready to be soldered on, with the wire from the spring connecting with one pad, and the base of the pin onto the other pad. Because the pins were bent from the previous step, a fair amount of adjustment had to be performed to ensure the short only occurred when the sensors were triggered. The antennae alone took at least as long as the rest of the assembly combined.

<div id="attachment_149" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2011/12/dscf2801.jpg"><img class="size-medium wp-image-149" title="DSCF2801" src="/wp-content/uploads/2011/12/dscf2801.jpg?w=300" alt="The finished Photopopper with curled antennae" width="300" height="185" srcset="/wp-content/uploads/2011/12/dscf2801.jpg 3111w, /wp-content/uploads/2011/12/dscf2801-300x185.jpg 300w, /wp-content/uploads/2011/12/dscf2801-1024x634.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The finished Photopopper with curled antennae
  </p>
</div>

After a fair amount of testing, I found that the antennae worked best when curled around, otherwise they would often spring past an obstacle, and fail to provide continued avoidance behaviour.

The last issue with this kit is that the solar panel it uses works extremely well in direct sunlight, but for us Canadians direct sunlight is in short supply this time of year. The alternative is to use an incandescent light bulb (florescent and halogen bulbs wont work), but these days incandescent lightbulbs are not so common. Luckily I was able to find an old desk lamp and incandescent bulb to use for testing and tuning. The video below shows some of this testing, in which the robot turns around to face the light source, then moves forward a short distance. This process slowly repeats itself. Obstacle avoidance is harder to fine tune, as the antennae often get stuck in the shorted position if mishandled. The problem of antennae springing past obstacles and not providing persistent avoidance still exists after they have been curled, though it&#8217;s less common.

Despite the issues encountered, this kit was very fun, and it was a great way to test out a new soldering iron. That being said; from start to finish it took much longer than the 2 hours they estimate in the instruction manual, and I can only imagine how difficult it would be with a cheap &#8220;fire starter&#8221; stick iron.
