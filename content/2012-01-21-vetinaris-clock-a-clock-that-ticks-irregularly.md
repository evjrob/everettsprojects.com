+++
title = "Vetinari's Clock: A Clock that Ticks Irregularly"
description = "My implementation of Simon Inn's Vetinari clock. Using a microcontroller the clock ticks irregularly but maintains accurate time."
date = 2012-01-21T19:32:54+00:00
authors = ["Everett Robinson"]
aliases = ["/2012/01/21/vetinaris-clock-a-clock-that-ticks-irregularly/"]

[taxonomies]
tags = [
    "Clocks",
    "Electronics",
    "PIC Microcontrollers",
    "Terry Pratchett",
    "Vetinari"
]

[extra]
id = 165
layout = "post"
guid = "http://ejrob.wordpress.com/?p=165"
dsq_thread_id = "6140711590"
image = "/wp-content/uploads/2012/01/dscf2871-672x372.jpg"
comments = true
+++

<p style="text-align: left;">
  I saw this sort of project posted on Hackaday a few months ago, <a href="http://hackaday.com/2011/10/06/vetinari-clock-will-drive-you-insane/">originally using an Arduino</a>, and quickly went to work building my own. It worked well when plugged into the USB port of my computer, and I was excited to hook it up to some batteries and see how long it would run (knowing full well that the Arduino was probably going to run them dry fairly quickly). It made it about 36 hours before the clip of 5 AA batteries was drained, and so I decided to try and rig it up with a 9V wall adapter power supply. Unfortunately, for reasons I am still unsure of, the whole thing would stop ticking after exactly 38 seconds and I quickly gave up in frustration. Luckily for me, Simon Inns came up with <a href="https://www.waitingforfriday.com/?p=264">a version using a PIC microcontroller</a> that runs much longer on only 2 AA batteries. Having never used PIC microcontrollers, I decided this was a good opportunity to learn something about them and used some money received at Christmas to order the parts and tools necessary for my own version of this clock.
</p>

<div id="attachment_169" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2012/01/dscf2825.jpg"><img class="size-medium wp-image-169" title="DSCF2825" src="/wp-content/uploads/2012/01/dscf2825.jpg" alt="The components necessary to make it work" width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2825.jpg 3664w, /wp-content/uploads/2012/01/dscf2825-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2825-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The components necessary to make it work
  </p>
</div>

<p style="text-align: left;">
  Each clock requires a PCB, a PIC 12F683 microcontroller, two Schottkey diodes (1N5819), two 47Ω resistors, two 22pF capacitors, one 100nF capacitor, a 32.768 kHz crystal, and a 6 pin 0.1″ header of some sort for programming (I used a male right angle header). It is also a good idea to use a DIP socket for the PIC microcontroller, so that it can easily be removed if necessary. Using the Cadsoft Eagle schematics and board files supplied by Simon Inns, I slightly rerouted one of the traces so that it would pass the DRC Bot (an automated program to check that prototype boards conform to the rules) at BatchPCB.com and ordered a couple of the boards. I was pleasantly surprised when they arrived and I found 4 boards, all of which appeared to be in perfect condition. Altogether, the materials necessary for a single clock cost less than $20 (not including the tools to program the PIC or the shipping fees).
</p>

<div style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2012/01/dscf2833.jpg"><img class="wp-image-171 " title="DSCF2833" src="/wp-content/uploads/2012/01/dscf2833.jpg" alt="The PCB with components soldered in place" width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2833.jpg 3664w, /wp-content/uploads/2012/01/dscf2833-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2833-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The PCB with components soldered in place
  </p>
</div>

<p style="text-align: left;">
  I started by soldering everything to the PCB which was straight forward, though the capacitors I purchased were different from the ones originally used by Simon Inns, and I had to bend the leads to make them fit. The picture to the right shows all of the components soldered into place, with the exception of the leads for the clock and battery clip. It is also important to make sure the Diodes are installed in the correct direction, or else they will not properly protect the microcontroller from the flyback voltage that is generated by the solenoid in the clock mechanism.
</p>

<p style="text-align: left;">
  Next it is necessary to dissect the clock, and hook up the solenoid that drives it to our circuitry instead of the little board that normally drives it. In theory this is simply done by cutting the traces to the little pads near the bottom where the solenoid attaches, and then soldering our own wires to it, though the board inside the clock is cheap, and the copper pad itself delaminated from the board almost immediately upon trying this.
</p>

<div id="attachment_178" style="width: 280px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2012/01/dscf2857.jpg"><img class=" wp-image-178 " title="DSCF2857" src="/wp-content/uploads/2012/01/dscf2857.jpg" alt="The left copper pad has delaminated from the board" width="270" height="203" srcset="/wp-content/uploads/2012/01/dscf2857.jpg 3664w, /wp-content/uploads/2012/01/dscf2857-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2857-1024x768.jpg 1024w" sizes="(max-width: 270px) 100vw, 270px" /></a>

  <p class="wp-caption-text">
    The left copper pad has delaminated from the board
  </p>
</div>

<div id="attachment_176" style="width: 280px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2012/01/dscf2843.jpg"><img class=" wp-image-176  " title="DSCF2843" src="/wp-content/uploads/2012/01/dscf2843.jpg" alt="The guts of the clock mechanism" width="270" height="203" srcset="/wp-content/uploads/2012/01/dscf2843.jpg 3664w, /wp-content/uploads/2012/01/dscf2843-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2843-1024x768.jpg 1024w" sizes="(max-width: 270px) 100vw, 270px" /></a>

  <p class="wp-caption-text">
    The guts of the clock mechanism
  </p>
</div>

<div style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2012/01/dscf2858.jpg"><img class=" wp-image-179 " title="DSCF2858" src="/wp-content/uploads/2012/01/dscf2858.jpg" alt="Everything rewired to the battery contacts, and hot glued" width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2858.jpg 3664w, /wp-content/uploads/2012/01/dscf2858-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2858-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    Everything rewired to the battery contacts, and hot glued
  </p>
</div>

Not to be defeated, I simply rerouted the thin wires of the solenoid to the large copper pads that were formerly the contact points for the battery, and made all of my connections there. I followed that with plenty of hot glue to keep everything firmly in place, and then went about putting the clock mechanism back together. Unfortunately for me I neglected to double check that everything was functioning before I glued it, which caused some issues later. Lesson learned: check your solder joints BEFORE you smother them in glue.

<div id="attachment_181" style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2012/01/dscf2864.jpg"><img class="size-medium wp-image-181" title="DSCF2864" src="/wp-content/uploads/2012/01/dscf2864.jpg" alt="All of the clockwork put back in place." width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2864.jpg 3664w, /wp-content/uploads/2012/01/dscf2864-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2864-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    All of the clockwork put back in place.
  </p>
</div>

<p style="text-align: left;">
  In order to reassemble the clock, I had to cut a notch in the housing to make space for the leads I had just soldered on, and I also trimmed off most of the plastic that formed the original battery holder, since it was no longer necessary. After replacing the back plate and soldering the battery leads (make sure the polarity is correct!) and the clock leads in place on the PCB, I then hot glued everything to the back of the clock and stuck in a couple of batteries.
</p>

<div id="attachment_174" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2012/01/dscf2840.jpg"><img class="size-medium wp-image-174" title="DSCF2840" src="/wp-content/uploads/2012/01/dscf2840.jpg" alt="The original clock used with the arduino, now being run by the same circuit on a breadboard" width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2840.jpg 3664w, /wp-content/uploads/2012/01/dscf2840-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2840-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The original clock used with the arduino, now being run by the same circuit on a breadboard
  </p>
</div>

<p style="text-align: left;">
  This was the point at which I realized something had gone wrong, since the clock was not ticking like the one I had already assembled using a breadboard. At first I was worried that one of the components on the PCB had been fried, but my trusty multimeter assured me otherwise when I saw pulses of voltage at the point where the clock leads had been soldered onto the PCB. This was were I realized that the problem must exist at the solder joints in the clock, which I had already hot glued. Oops! Luckily I already had a functioning clock mechanism from back when I assembled my power hungry Arduino version, which I had already hooked up to the breadboard version seen left. I cut the leads between the clock and the PCB, and swapped out the broken clock mechanism for the functioning one. Since both clocks were the same, this was a trivial task (thankfully).
</p>

<div id="attachment_183" style="width: 310px" class="wp-caption alignright">
  <a href="/wp-content/uploads/2012/01/dscf2870.jpg"><img class="size-medium wp-image-183" title="DSCF2870" src="/wp-content/uploads/2012/01/dscf2870.jpg" alt="The functioning clock, with swapped clock mechanism" width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2870.jpg 3664w, /wp-content/uploads/2012/01/dscf2870-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2870-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    The functioning clock, with swapped clock mechanism
  </p>
</div>

<p style="text-align: left;">
  Finally the clock was assembled and functioning, and I used some more hot glue to hold everything in place, including all of the wires. I also strategically positioned the PCB so the 6 pin programming headers would face downwards for easy access. Uploading the program the PIC is fairly easy, and I accomplished it without any issues by using the PICKit 3 with Microchip&#8217;s MPLAB X IDE. At the same time, I decided to re-brand the clock (no name dollar store brands don&#8217;t cut it) using some stickers I got when I ordered the components. I have had the clock running on a fresh pair of AA batteries since January 11th, 2012, and while it fell behind the clock on my computer by 10 seconds in the first two days, it has maintained accurate time since. My plan now is to leave it on my wall and test how long it runs on a pair of batteries and to compare that to the back of the envelope calculation I did earlier, which predicted at least 60 days for lower capacity batteries. While I have not yet noticed any brain mushification as a result of the clock, it seems like it disrupts my sleep slightly by causing me to wake more often during the night. We&#8217;ll see whether the batteries or my patience for poor sleep give out first.
</p>

<div id="attachment_184" style="width: 310px" class="wp-caption alignleft">
  <a href="/wp-content/uploads/2012/01/dscf2871.jpg"><img class="wp-image-184 size-medium" title="DSCF2871" src="/wp-content/uploads/2012/01/dscf2871-300x225.jpg" alt="Re-branded and fully functioning!" width="300" height="225" srcset="/wp-content/uploads/2012/01/dscf2871-300x225.jpg 300w, /wp-content/uploads/2012/01/dscf2871-1024x768.jpg 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>

  <p class="wp-caption-text">
    Re-branded and fully functioning!
  </p>
</div>

While over simplified, the circuit is basically 2 47Ω resistors in series, for a total of 94Ω. It operates at 3V, so the current draw is 3V/94Ω = 0.0319A = 31.9mA. But the clock mechanism is only powered for 30ms for each tick, which on average occur once per second, so the average current draw is 31.9mA * 30ms/1000ms = 0.957mA. The PIC microcontroller draws 11μA at 32kHz, which is essentially negligible in such a rough calculation. Rounding the average current draw up to 1mA, and assuming a cheap set of AA batteries with 1500mAh capacity, the clock should theoretically run for 1500 hours, which works out to 62.5 days. For a  better set of batteries with 2500mAh capacity, we get 2500 hours of operation, or about 104 days. In either case, two AA batteries every 2 to 3 months is far better than 5 AA batteries every 36 hours. **EDIT: The clock managed to go for about 5 months on a pair of batteries before it became noticeably slow. It was 10 minutes behind the correct time when I finally replaced its batteries.**