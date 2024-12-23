export async function onRequest(context) {
    return new Response(
      JSON.stringify({
        "body": "No."
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