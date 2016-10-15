#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://fazendanatureza.com/bot/botarz.php"
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):
    row1_title = data[0]['title']
    row1_subtitle = data[0]['subtitle']
    row1_img_url = data[0]['img_url']
    row1_web_url = data[0]['web_url']
    if row1_title is None:
        return {}
    row2_title = data[1]['title']
    row2_subtitle = data[1]['subtitle']
    row2_img_url = data[1]['img_url']
    row2_web_url = data[1]['web_url']

    # print(json.dumps(item, indent=4))

    speech = "This is the response from server... " + row1_title + row1_subtitle + row1_img_url + row1_web_url+row2_title + row2_subtitle + row2_img_url + row2_web_url
    print("Response:")
    print(speech)
    message= {
      "attachment": {
         "type": "template",
          "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row1_title,
               "subtitle": row1_subtitle,
               "item_url": row1_web_url,               
               "image_url": row1_img_url ,
                "buttons": [{
                "type": "web_url",
                "url": row1_web_url,
                "title": "Open Web URL"
            }, 
                    {
                "type": "postback",
                "title": "Call Postback",
                "payload": "Payload for first bubble",
            }],
          }, 
                   {
                "title": row2_title,
                "subtitle": row2_subtitle,
                "item_url": row2_web_url,               
                "image_url": row2_img_url,
                "buttons": [{
                "type": "web_url",
                "url": row2_web_url,
                "title": "Open Web URL"
            },
                    {
                "type": "postback",
                "title": "Call Postback",
                "payload": "Payload for second bubble",
            }]
          }]
        }
      }
    }

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"facebook": message},
        # "contextOut": [],
        #"source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
