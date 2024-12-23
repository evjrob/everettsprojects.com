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
  const accountedFor = new Array(secretCode.length).fill(false);
  let whiteList = [...secretCode];

  // Check for exact matches (black)
  for (let i = 0; i < secretCode.length; i++) {
    if (guess[i] === secretCode[i]) {
      score.push('black');
      accountedFor[i] = true;
      whiteList = whiteList.filter((val, idx) => idx !== i);
    }
  }

  // Check for correct color wrong position (white)
  for (let i = 0; i < secretCode.length; i++) {
    if (!accountedFor[i] && whiteList.includes(guess[i])) {
      score.push('white');
      const index = whiteList.indexOf(guess[i]);
      whiteList.splice(index, 1);
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