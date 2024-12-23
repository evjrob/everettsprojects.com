export async function onRequest(context) {
    const correctResponse = ['A','D','F','A','D','F','A','C','B',
                            'G','F','G','A','D','C','E','D'];
    const successMessage = [
      "Congratulations!", 
      "Bozley prefers a different tune, but he'll give you your next puzzle anyway. Go find him!",
      "Remember this code: MUTT"
    ];
  
    // Get the guess from the POST data
    const { guess } = await context.request.json();
    let solved = false;
    let message = ["Nope. That's not it"];
    
    if (JSON.stringify(guess) === JSON.stringify(correctResponse)) {
      solved = true;
      message = successMessage;
    }
    
    return new Response(
      JSON.stringify({
        solved: solved,
        message: message
      }), 
      {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': 'true'
        }
      }
    );
  }