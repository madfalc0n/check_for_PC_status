import json
# import slackclient
import requests as req


def post_slack(url,msg):
    webhook_url = url
    message = json.dumps(msg)
    response = req.post(webhook_url, data=message, headers= {'Content-Type' : 'application/json'})
    print(response.status_code)


test_block = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "This is a plain text section block.",
                            "emoji": True
                        }
                    }
                ]
            }

url = 'my slack webhook url'
msg = test_block
post_slack(url,msg)
