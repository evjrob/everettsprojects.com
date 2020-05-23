import json


# sample secret code and guess
allowed_symbols = ["1", "2", "3", "4", "5", "6"]
secret_code = ["2", "4", "2", "6", "1"]
color_map = {
    "1": "brown",
    "2": "blue",
    "3": "yellow",
    "4": "red",
    "5": "green",
    "6": "orange",
}
success_message = ["Congratulations!", "Now you must head to the lion's den.", 
    "What, you want better directions? Fine:", "evaporates.unmarried.captions",
    "Need another hint?", "filled.count.soap"]


# based on https://codereview.stackexchange.com/questions/111637/mastermind-evaluating-the-guess
def evaluate_guess(secret_code, guess):
    score = []
    accounted_for = [False,] * len(secret_code)
    white_list = []

    for i in range(len(secret_code)):
        if guess[i] == secret_code[i]:
            score.append('black')
            accounted_for[i] = True
        else:
            white_list.append(secret_code[i])

    for i in range(len(secret_code)):
        if guess[i] in white_list and not accounted_for[i]:
            score.append('white')
            white_list.remove(guess[i])
    
    score.sort()
    
    if len(score) < len(secret_code):
        score = score + ['grey',] * (len(secret_code) - len(score))

    return score


def lambda_handler(event, context):
    # Get the guess from the POST data
    guess = json.loads(event['body'])['guess']

    solved = False
    score = []
    message = [""]
    
    
    score = evaluate_guess(secret_code, guess)
    if score == ['black'] * len(secret_code):
        solved = True
        score = [color_map[s] for s in secret_code]
        message = success_message
    if not all((x in allowed_symbols) for x in guess):
        message = ["Are you sure you\'ve figured out this puzzle?"]
    
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials" : True 
        },
        "body": json.dumps({
            "guess": guess,
            "solved": solved,
            "score": score,
            "message": message
        })
    }

    return response