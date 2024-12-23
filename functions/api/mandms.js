const allowedSymbols = ["1", "2", "3", "4", "5", "6"];
const secretCode = ["2", "4", "2", "6", "1"];
const colorMap = {
  "1": "brown",
  "2": "blue",
  "3": "yellow",
  "4": "red",
  "5": "green",
  "6": "orange",
};
const successMessage = [
  "Congratulations!",
  "Now you must head to the lion's den.",
  "What, you want better directions? Fine:",
  "evaporates.unmarried.captions",
  "Need another hint?",
  "filled.count.soap"
];

function evaluateGuess(secretCode, guess) {
  const score = [];
  const secretAccountedFor = new Array(secretCode.length).fill(false);
  const guessAccountedFor = new Array(secretCode.length).fill(false);

  // Check for exact matches (black)
  for (let i = 0; i < secretCode.length; i++) {
    if (guess[i] === secretCode[i]) {
      score.push('black');
      secretAccountedFor[i] = true;
      guessAccountedFor[i] = true;
    }
  }

  // Check for correct color wrong position (white)
  for (let i = 0; i < guess.length; i++) {
    if (guessAccountedFor[i]) continue; // Skip if this position was used for a black peg
    
    // Look for a matching number in the secret code that hasn't been used yet
    for (let j = 0; j < secretCode.length; j++) {
      if (!secretAccountedFor[j] && guess[i] === secretCode[j]) {
        score.push('white');
        secretAccountedFor[j] = true;
        guessAccountedFor[i] = true;
        break;
      }
    }
  }

  score.sort();

  // Fill remaining spots with grey
  while (score.length < secretCode.length) {
    score.push('grey');
  }

  return score;
}

export async function onRequest(context) {
  try {
    const request = context.request;
    const body = await request.json();
    const guess = body.guess;

    let solved = false;
    let score = [];
    let message = [""];

    score = evaluateGuess(secretCode, guess);
    if (score.every(s => s === 'black')) {
      solved = true;
      score = secretCode.map(s => colorMap[s]);
      message = successMessage;
    }
    if (!guess.every(x => allowedSymbols.includes(x))) {
      message = ["Are you sure you've figured out this puzzle?"];
    }

    return new Response(
      JSON.stringify({
        guess,
        solved,
        score,
        message
      }), 
      {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': 'true'
        }
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Invalid request' }), 
      { 
        status: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': 'true'
        }
      }
    );
  }
}