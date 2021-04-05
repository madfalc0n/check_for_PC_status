"""
MESSAGE POST to Slack
"""

import json
import requests as req


# msg_form = {
#                 "blocks": [
#                     {
#                         "type": "section",
#                         "text": {
#                             "type": "plain_text",
#                             "text": "This is a plain text section block.",
#                             "emoji": True
#                         }
#                     }
#                 ]
#             }

msg_form = {"text": "This is a plain text section block."}

def post_slack(url,msg):
    global msg_form

    webhook_url = url
    
    # msg_form['blocks'][0]['text']['text'] = msg
    msg_form['text'] =msg

    message = json.dumps(msg_form)
    response = req.post(webhook_url, data=message, headers= {'Content-Type' : 'application/json'})
    # print(response.status_code)
    result = int(response.status_code)
    return result

#test mode
if __name__ == "__main__":
    url = 'YOUR SLACK WORKSPACE CODE'
    test_msg = 'ON'
    post_slack(url, test_msg)