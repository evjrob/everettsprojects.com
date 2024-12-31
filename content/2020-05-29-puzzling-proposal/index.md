+++
title = "A Puzzling Proposal"
description = "The set of puzzles I designed and made my fiance solve to find the site of my marriage proposal. Can you solve them?"
date = "2020-05-29"
authors = [ "Everett Robinson",]
aliases = ["/2020/05/29/puzzling-proposal.html"]

[taxonomies]
tags = ["Proposal", "Puzzles", "Arduino"]

[extra]
layout = "post"
output = "html_document"
+++

<style>
 /* Style the button that is used to open and close the collapsible content */
.collapsible {
  background-color: #eee;
  color: #444;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

/* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
.active, .collapsible:hover {
  background-color: #ccc;
}

/* Style the collapsible content. Note: hidden by default */
.content {
  display: none;
} 
</style>

Back in September 2019 I proposed to my girlfiend of three and a half years! She said yes. I have no idea why, because I literally made her and her best friend solve a series of puzzles just to find me. I'm glad she didn't give up, and wasn't fed up with me by the end of it. Without further delay, here is a subset of the most interesting puzzles:

### Puzzle 1

You're presented with a small box containing:

* M&Ms: 1 Brown, 2 Blue, 3 Yellow, 4 Red, 5 Green, and 6 Orange ones.
* A URL: <a href='http://everettsprojects.com/8543W/mandms/'>http://everettsprojects.com/8543W/mandms/</a>
* A note: "Hmm... I can't remember the code. I think it started with blue? No that's not right... Oh well, there's only 7,776 combinations!"


<button class="collapsible" id="puzzle1">Click here to see the solution.</button>

<div class="content" id="puzzle1solution">
  <p>
    The puzzle is a simple clone of the game Mastermind. The colors are a bit of a red herring, with the varying numbers meant to make you think about using digits. The cheeky note is only there to encourage experimentation. The solution to the mastermind puzzle is 24261. Blue Red Blue Orange Brown. But you figured that out on your own, right?`
  </p>
  <p>
    In the next stage the three words are a what3words address. The lion's den is the home of my sister, a co-conspirator, and the lion is her cat Leo. The next puzzle is waiting.
  </p>
</div>


### Puzzle 2

You arrive at the next puzzle to find only this:

![Puzzle 2](puzzle2.png)

<button class="collapsible" id="puzzle2">Click here to see the solution.</button>

<div class="content" id="puzzle2solution">
  <p>
    It's a KenKen puzzle which is then used as a one time pad to decode the text: "Home Office Arduino Code NOTE":
  </p>
  <img src='puzzle2solution.png'/>
  <p>
    You know where to go.
  </p>
</div>

### Puzzle 3

You find a box with a letter combination lock. It opens with the code "NOTE" and you find an arduino:

<iframe width="725" height="453" src="https://www.tinkercad.com/embed/jJDQAT2PAjE" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

<br>
There is also another URL: <a href='http://everettsprojects.com/8543W/song-time/'>http://everettsprojects.com/8543W/song-time/</a>

Nothing more is provided.

<button class="collapsible" id="puzzle3">Click here to see the solution.</button>

<div class="content" id="puzzle3solution">
  <p>
    You might recognize the melody as the Song of Time from the Legend of Zelda: Ocarina of Time. If you play the corresponding notes <strong>"A,D,F,A,D,F,A,C,B,G,F,G,A,D,C,E,D"</strong> without errors and press submit you are told the location of the next clue lies with my family dog Bozley and receive another code word: MUTT.
  </p>
</div>

### Puzzle 4

You find two locked boxes. The first has a direction lock. The second expects a four letter code and the word MUTT opens it. Inside you find:

1.) A Rubik's cube covered in arrows. It didn't come pre-solved, so you could solve one before proceeding if you would like the full experience:

![Rubiks Cube](puzzle4rubiks.png)

2.) The following diagram:

![Puzzle 4](puzzle4.png)

<button class="collapsible" id="puzzle4">Click here to see the solution.</button>

<div class="content" id="puzzle4solution">
  <p>
    The codes on the diagram are different ways of expressing colors:
      <ul>
        <li>あか: Japanese for Red</li>
        <li>9000K: The color temperature of Blue</li>
        <li>580nm: The wavelength of Yellow</li>
        <li>#FFA500: Hexadecimal RGB for Orange</li>
        <li>2 + 3: Blue + Yellow = Green</li>
        <li>blanc: French for White</li>
      </ul>  
    Matching the colors to the faces of the Rubik's cube and then choosing the arrows located in the same square in order of the circled numbers gives the code: Up Up Down Down Left Right.
  </p>
  <img src='puzzle4solution.png'/>
  <p>
    This code opens the direction lock and inside you find a <a href='https://www.youtube.com/watch?v=VIVIegSt81k'>hexahexaflexagon</a>. On the the many faces of the hexahexaflexagon is the location of the proposal site where I have been patiently waiting.
  </p>
</div>


<script>
var coll = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = document.getElementById(this.id+"solution");
    if (content.style.display === "inline") {
      content.style.display = "none";
    } else {
      content.style.display = "inline";
    }
  });
}
</script>