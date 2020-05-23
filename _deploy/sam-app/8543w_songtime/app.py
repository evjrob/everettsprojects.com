import json


correct_response = ['A','D','F','A','D','F','A','C','B',\
                    'G','F','G','A','D','C','E','D']
success_message = ["Congratulations!", 
    "Bozley prefers a different tune, but he'll give you your next puzzle anyway. Go find him!",
    "Remember this code: MUTT"]

def lambda_handler(event, context):
    # Get the guess from the POST data
    guess = event['guess']
    solved = False
    message = ["Nope. That's not it"]
    
    if guess == correct_response:
        solved = True
        message = success_message
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True 
        },
        "body": json.dumps({
            "solved": solved,
            "message": message
        })
    }

    return response