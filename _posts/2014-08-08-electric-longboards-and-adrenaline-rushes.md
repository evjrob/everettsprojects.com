---
id: 1076
title: Electric Longboards and Adrenaline Rushes
date: 2014-08-08T09:18:06+00:00
author: Everett
layout: post
guid: http://everett.x10.mx/?p=1076
permalink: /2014/08/08/electric-longboards-and-adrenaline-rushes/
dsq_thread_id:
  - "6140711856"
image: https://everettsprojects.com/wp/wp-content/uploads/2014/08/IMG_2494-672x372.jpg
categories:
  - Electronics
  - Kits
tags:
  - BLDC motor
  - Electric
  - ESC
  - LiPo batteries
  - Longboard
  - Motorized skateboard
  - Pure Awesomeness
  - Skateboard
---
  1. [Why pursue this madness?](#why)
  2. [The parts](#parts)
  3. [Putting it all together](#assembly)
  4. [The results](#results)

<div id="attachment_1156" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/08/IMG_2495.jpg"><img class="size-large wp-image-1156" src="http://everett.x10.mx/wp/wp-content/uploads/2014/08/IMG_2495-1024x768.jpg" alt="The final board" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/08/IMG_2495-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/08/IMG_2495-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    A side shot of the final board.
  </p>
</div>

&nbsp;

<div id="why">
  <strong>Why pursue this madness?</strong>
</div></p> 

<div>
  Like many of my projects, it all started when I stumbled upon something interesting on the internet. In this case it was a <a href="https://www.youtube.com/watch?v=2KtMCX7FfZ0">video of the Board of Imagination</a>. Now, a mind controlled skateboard is pretty cool, and arguably the main point of interest in that project. But it was the motorization of the board that really captivated me. Motorizing skateboards is really nothing new, in fact the use of a normal DC motor and gears in the Board of Imagination is pretty old school. It&#8217;s essentially all Brushless DC motors (BLDC) and timing belts now. There are also <a href="http://endless-sphere.com/forums/">entire communities built around achieving and refining the goal of motorized anything</a>. And it was that little bit of research that did me in. I no longer just wanted one; I <em>needed</em> one.
</div>



<div>
  I spent a lot of time working out the logistics of motorizing a longboard, and explored all of the options. There was the expensive but very slick looking <a href="https://www.redrockboardshop.com/2013-05-12-04-30-16/lagrange-l1-specs">LaGrange L1 truck</a>. The pretty venerable looking <a href="http://www.aliendrivesystems.com/">Alien Drive System</a> and <a href="http://alienpowersystem.com/">Alien Power System</a> combo. Last of all, there was the very sturdy looking one piece Paris truck with welded on motor mount provided at <a href="http://diyelectricskateboard.com/">http://diyelectricskateboard.com/</a>. The DIY Electric Skateboard kit looked to be the newest kid on the block, and didn&#8217;t really have as much in the way of reviews. But it looked like it was the most approachable in terms of repairs and tinkering, and that&#8217;s what sold me on it. Or on the design at least.
</div>



<div>
  Originally my plan had been to weld a similarly styled, but self designed and fabricated motor mount to a set of Paris Trucks. I knew the equipment at <a href="http://protospace.ca/">Protospace</a> (the local makerspace) was capable of it, but I lacked the skill set to use any of those tools. It became obvious to me that I would need to simply buy the pre-made trucks if I wanted to have my board running before the end of summer. It was a good call, because with that part of the project taken care of, the rest of it quickly progressed, and I now have a functioning motorized longboard.
</div>



<div>
  But enough talking, lets look at the process of building such a toy. S<em>eriously though, this board has an insane amount of power. It can accelerate way too fast and reach a top speed well above my current comfort level of about 30km/h. Don&#8217;t treat it like a toy.</em>   <strong> </strong>
</div>

&nbsp;

<div id="parts">
  <strong>The parts:</strong>
</div>



  1.  A longboard deck. _I used the [Earthwing Big Hoopty](http://www.earthwingboards.com/#!store/c2fv). It&#8217;s a super solid and awesome board at an easy $107 from a local board shop._
  2. The trucks and drive mechanism from [DIYelectricskateboard.com](http://diyelectricskateboard.com/product/single-motor-electric-longboard-kit/).
  3. Some bearings, as they don&#8217;t come with the DIY Electric kit.
  4. A [brushless DC motor](http://www.hobbyking.com/hobbyking/store/__18180__Turnigy_Aerodrive_SK3_6364_213kv_Brushless_Outrunner_Motor.html).
  5. An Electronic Speed Controller to run the motor. _I took a risk on this [Boat ESC](http://www.hobbyking.com/hobbyking/store/__28224__HobbyKing_120A_Boat_ESC_4A_UBEC.html). The braking is a little soft, but it runs well, barely gets warm even without proper cooling, and doesn&#8217;t make excess noise._
  6. At least one battery pack. _A 5000 mAh 6S (22.2V) provides plenty of speed and power. I used two [3S batteries](http://www.hobbyking.com/hobbyking/store/__8579__ZIPPY_Flightmax_5000mAh_3S1P_20C.html) in series to make a 6S battery with a lower profile. _
  7. A receiver and transmitter of some sort. I used the all too common [Quanum (nope, not a typo) pistol grip combo](http://www.hobbyking.com/hobbyking/store/__44693__Quanum_2_4Ghz_3ch_Pistol_Grip_Tx_Rx_System.html).
  8. RC connectors. _I used [HXT4mm](http://www.hobbyking.com/hobbyking/store/__9283__HXT_4mm_Gold_Connector_w_Protector_10pcs_set_.html) to be consistent with the existing connectors._
  9. Some way to attach the parts to the deck. I used [industrial strength Velcro tape](http://www.homedepot.ca/product/velcro-industrial-strength-4-ft-x-2-in-tape/967153#BVRRWidgetID).
 10. Some way to shield the LiPo batteries from damage by debris. I tried using ABS, gave up, and resorted to a box made from [22 gauge galvanized steel sheet](http://www.homedepot.ca/product/8x24sheet-metal-22g-galvanized/955471).

&nbsp;

<div id="assembly">
  <strong>Putting it all together:</strong>
</div>



<div>
  The process of putting together isn&#8217;t all that difficult. With the step requiring the welding of a motor mount to a truck eliminated, the most difficult part was definitely the construction of the battery shield. But we get ahead of ourselves. Lets start with the deck and trucks.
</div>

<div id="attachment_1090" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2460.jpg"><img class="wp-image-1090 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2460-1024x768.jpg" alt="IMG_2460" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2460-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2460-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The longboard deck with trucks and wheels attached.
  </p>
</div>

The first step of mounting the trucks is very straight forward. If you have ever assembled a normal skateboard or longboard before, then you already know what to do. For those who haven&#8217;t put together a board, I&#8217;ll cover the basics. The easiest place to start is inserting the bearing into the ABEC 11 Flywheel clones. [This is just a matter of putting one bearing onto the axle, then pressing the wheel down onto it.](https://www.youtube.com/watch?v=FN8kFgmMhTU) Repeat this process for each side of each wheel. Once the wheels are set up, you can fasten them to the trucks with the appropriate nut. Ensure the wheel with the plastic timing belt pulley goes on the correct side of the truck with the motor mount. Tighten the nuts just enough to remove any play along the axle. Finally, you can bolt the trucks to the long board deck. This is very straight forward, you just need to use provided bolts and nylon lock nuts, and ensure that the kingpin is facing outward.

<div id="attachment_1091" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2461.jpg"><img class="wp-image-1091 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2461-1024x768.jpg" alt="IMG_2461" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2461-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2461-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The motor pulley. Note the two holes for set screws.
  </p>
</div>

With the basic hardware mounted, we can set up the motor too. Notice that the provided timing belt pulley for the motor has two bolts to tighten it to the motor shaft. It&#8217;s very helpful to have a couple  of flat spots on the motor shaft for these bolts to fasten against.

<div id="attachment_1092" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2462.jpg"><img class="wp-image-1092 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2462-1024x768.jpg" alt="IMG_2462" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2462-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2462-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The brushless DC motor shaft has been dremeled down to make flat spots for the set screws.
  </p>
</div>

I achieved this by using a Dremel tool with a carbide bit. I recommend that you punch the motor shaft through a piece of paper towel before grinding the flat spots in, as the metal filings are going to be magnetized and get stuck to the shaft. The paper towel allows you to easily wipe them all away.

<div id="attachment_1094" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2464.jpg"><img class="wp-image-1094 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2464-1024x768.jpg" alt="IMG_2464" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2464-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2464-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The BLDC motor has been attached to the mounting bracket. It&#8217;s still loose enough to slide in the slots.
  </p>
</div>

Attaching the motor pulley is pretty easy, but first we need to losely fit the motor to the motor mount. You want to attach the motor so that it&#8217;s flush with the motor mount, but still just lose enough to slide in the slots. We need it loose to tension the motor after we put the pulleys and belt on. The motor pulley is really easy. Just line the bolts up with the Dremelled down spots and tighten them using an Allen Key.  Once that is done, the timing belt can be added. If everything is still a little lose, then it will be as simple as just slipping it over the wheel and then the motor pulley.

<div id="attachment_1095" style="width: 484px" class="wp-caption alignnone">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2465.jpg"><img class="wp-image-1095 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2465-1024x768.jpg" alt="IMG_2465" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2465-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2465-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The belt is now in place and ready for tensioning.
  </p>
</div>

Finally, we need to tension the belt. This is achieved by pulling the motor along the mount until the belt is firm, but not excessively tight, then tightening the four M4 socket head bolts that hold the motor to the mount. This is also not a bad time to adjust the tightness of the bushings on the trucks (the plasticy coloured parts on the kingpin). Just loosen them until you find it steers well, but without any contact between the wheels and the board.

<div id="attachment_1096" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2466.jpg"><img class="wp-image-1096 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2466-1024x768.jpg" alt="IMG_2466" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2466-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2466-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The belt has been pulled taught and the motor has been tightened onto the mounting bracket.
  </p>
</div>

And that&#8217;s it for the Mechanical side of things. Next up is the electronics and the protective shield for the electronics.

<div id="attachment_1097" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2467.jpg"><img class="wp-image-1097 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2467-1024x768.jpg" alt="IMG_2467" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2467-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2467-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The ESC has had the connectors soldered on and is plugged into the motor.
  </p>
</div>

The electronics are also pretty straight forward. For the most part it is all just plug and play, with the exception of the ESC, which requires one to solder on the connector of their choice. Since everything else I ordered is using the HXT4 mm bullet connectors, I simply stuck with those. I hacked three of them apart to create three stand alone female connectors for the motor, and used a full one for the power connection. It&#8217;s important to make sure you get the polarity right, so match up the wire colours with one of the batteries to be sure you solder it on the right way. The insulation on the wire is also too large for the red plastic housing, so I stripped it back a little bit to solder the connector on before putting it back in place and taping the insulation back up. I used tape because I forgot to put some heat shrink tubing on before the connector. Don&#8217;t make the same silly mistake, and remember the heat shrink tubing!

Now it&#8217;s just a matter of plugging everything together and attaching it to the bottom of the board. I hooked everything together and made sure the motor worked first, then I set to work planning the layout of the components on the underside of the board. Once I was satisfied I used the industrial strength adhesive Velcro tape to hold everything in place. It has a 2 inch width which is exactly the right width for the ESC and batteries. At this point the board is technically ridable, but LiPo batteries have a reputation for being a little &#8220;explodey&#8221; if they are damaged, so I wanted to play it safe and put a shield of sorts over them.

<div id="attachment_1081" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/DSCF0230.jpg"><img class="wp-image-1081 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/DSCF0230-1024x768.jpg" alt="DSCF0230" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/DSCF0230-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/DSCF0230-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The failed ABS plastic shield. ABS is a finicky material.
  </p>
</div>

Building the shield was the hardest and most frustrating part. I had originally planned to construct it out of .25&#8243; ABS sheet, but that failed spectacularly. Apparently ABS plastic is renowned for its tendency to warp as it cools (it&#8217;s why 3D printers using ABS need heated base plates), and may not be the ideal material to learn on the fly without prior experience. I tried to make it work with just a heat gun, but that wasn&#8217;t going to work, so I resorted to slump forming the sheet in an oven.That also didn&#8217;t work. ABS is a pain, it&#8217;s no wonder it is usually moulded to a form using a vacuum.

After the failure of the ABS shield, I decided to try my hand at making a box out of sheet metal. I was able to get 8 inch wide 22 gauge galvanized steel from the local Home Depot, and I figured that I could pick up the sheet metal skill set a lot more easily.

<table style="border-style: none;">
  <tr style="border-style: none;">
    <td style="border-style: none;">
      <div id="attachment_1116" style="width: 235px" class="wp-caption aligncenter">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/SCAN0002a.jpg"><img class="wp-image-1116" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/SCAN0002a-300x186.jpg" alt="SCAN0002a" width="225" height="140" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/SCAN0002a-300x186.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/SCAN0002a-1024x635.jpg 1024w" sizes="(max-width: 225px) 100vw, 225px" /></a>
        
        <p class="wp-caption-text">
          The front panel that faces the direction of motion.
        </p>
      </div>
    </td>
    
    <td style="border-style: none;">
      <div id="attachment_1115" style="width: 235px" class="wp-caption aligncenter">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/SCAN0001a.jpg"><img class="wp-image-1115" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/SCAN0001a-300x218.jpg" alt="SCAN0001a" width="225" height="164" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/SCAN0001a-300x218.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/SCAN0001a-1024x746.jpg 1024w" sizes="(max-width: 225px) 100vw, 225px" /></a>
        
        <p class="wp-caption-text">
          The main body of the sheet metal shield.
        </p>
      </div>
    </td>
  </tr>
</table>

I designed a pattern, and cut it out of the sheet using some straight snips. Unfortunately my 8 inch wide sheet wasn&#8217;t wide enough to construct the box as a single piece as I had hoped, but I figured I could compensate  by making the forward facing panel separately, and attaching it to the rest of the box with flat lock seams. I didn&#8217;t even bother soldering the pieces together.

<table style="border-style: none;">
  <tr style="border-style: none;">
    <td style="border-style: none;">
      <div id="attachment_1109" style="width: 235px" class="wp-caption alignnone">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2488.jpg"><img class="wp-image-1109" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2488-300x225.jpg" alt="IMG_2488" width="225" height="169" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2488-300x225.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2488-1024x768.jpg 1024w" sizes="(max-width: 225px) 100vw, 225px" /></a>
        
        <p class="wp-caption-text">
          The front panel cut out of the sheet metal.
        </p>
      </div>
    </td>
    
    <td style="border-style: none;">
      <div id="attachment_1106" style="width: 235px" class="wp-caption alignnone">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2485.jpg"><img class="wp-image-1106" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2485-300x225.jpg" alt="IMG_2485" width="225" height="169" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2485-300x225.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2485-1024x768.jpg 1024w" sizes="(max-width: 225px) 100vw, 225px" /></a>
        
        <p class="wp-caption-text">
          Bending the main body of the box into shape.
        </p>
      </div>
    </td>
  </tr>
</table>

For the most part it worked. The shield isn&#8217;t beautiful, but it is sturdy. The front panel rattles a little on rough roads, but I can&#8217;t see any circumstances in which it would fall off. In retrospect, a 22 gauge steel box is probably overkill as far as shielding goes, but there&#8217;s also some risk of the metal causing a short if it didn&#8217;t stand up to an impact, so over kill is probably good in this case.
  


<div id="attachment_1112" style="width: 484px" class="wp-caption aligncenter">
  <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2491.jpg"><img class="wp-image-1112 size-large" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2491-1024x768.jpg" alt="IMG_2491" width="474" height="355" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2491-1024x768.jpg 1024w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2491-300x225.jpg 300w" sizes="(max-width: 474px) 100vw, 474px" /></a>
  
  <p class="wp-caption-text">
    The finished box. It&#8217;s not going to win any competitions, but it will protect the batteries.
  </p>
</div>


  
With the box complete, I drilled some holes in the base flanges, and then drilled some corresponding holes in the longboard deck when I had everything centred. Using 1.5&#8243; long flat head bolts and some matching wing nuts I can easily replace and remove the shield as needed.

<table style="border-style: none;">
  <tr style="border-style: none;">
    <td style="border-style: none;">
      <div id="attachment_1114" style="width: 160px" class="wp-caption aligncenter">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2493.jpg"><img class="wp-image-1114" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/IMG_2493-300x225.jpg" alt="IMG_2493" width="150" height="113" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2493-300x225.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/IMG_2493-1024x768.jpg 1024w" sizes="(max-width: 150px) 100vw, 150px" /></a>
        
        <p class="wp-caption-text">
          The holes drilled in the flanges so the box can be attached to the longboard deck.
        </p>
      </div>
    </td>
    
    <td style="border-style: none;">
      <div id="attachment_1080" style="width: 160px" class="wp-caption aligncenter">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/DSCF0229.jpg"><img class="wp-image-1080" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/DSCF0229-300x225.jpg" alt="DSCF0229" width="150" height="113" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/DSCF0229-300x225.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/DSCF0229-1024x768.jpg 1024w" sizes="(max-width: 150px) 100vw, 150px" /></a>
        
        <p class="wp-caption-text">
          The longboard deck has corresponding holes with bolts and wing nuts. Some foam has been added to the shield to cushion the batteries.
        </p>
      </div>
    </td>
    
    <td style="border-style: none;">
      <div id="attachment_1079" style="width: 160px" class="wp-caption aligncenter">
        <a href="http://everett.x10.mx/wp/wp-content/uploads/2014/07/DSCF0228.jpg"><img class="wp-image-1079" src="http://everett.x10.mx/wp/wp-content/uploads/2014/07/DSCF0228-300x225.jpg" alt="DSCF0228" width="150" height="113" srcset="https://everettsprojects.com/wp/wp-content/uploads/2014/07/DSCF0228-300x225.jpg 300w, https://everettsprojects.com/wp/wp-content/uploads/2014/07/DSCF0228-1024x768.jpg 1024w" sizes="(max-width: 150px) 100vw, 150px" /></a>
        
        <p class="wp-caption-text">
          The finished shield firmly bolted to the underside of the deck.
        </p>
      </div>
    </td>
  </tr>
</table>

<div id="results">
  <strong>The results:</strong>
</div></p> 

The final product of all this labour is an adrenaline rush. I&#8217;ve never taken a longboard downhill, so I really don&#8217;t have a taste for the high speed longboarding some people are accustomed to. But that&#8217;s okay because it means that I get a nice pleasant adrenaline rush when I manage to get this board above 30km/h . 



Forgive the poor quality of the video, I lack a GoPro, so I had to film it with my phone. This also had the side effect that I didn&#8217;t really want to get up to speed, it&#8217;s nerve racking enough already without the additional filmography concerns.

In general, the acceleration has a ton of punch and the brakes are quite soft, especially at lower speeds. At higher speeds they work a lot better, and will certainly get you down to a speed at which you can toe drag to slow down. If you&#8217;re going down a really steep hill you may find that the brakes are too weak to prevent the acceleration due to gravity, so act accordingly. If that means toe dragging the whole way or walking the board down the hill, then do it. It also helps to reprogram the ESC to fit your riding style. You can find the instructions here: <http://www.hobbyking.com/hobbyking/store/uploads/842133110X337002X22.pdf>

I ended up keeping all the defaults except the startup acceleration, which I set to 9 levels. This makes the acceleration a lot smoother, so you&#8217;re less likely to over do it and fall over backwards as the board rockets forward.