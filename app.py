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
    global city_names
    city_names=processlocation(req)
    global sector_names
    sector_names=processSector(req)
    baseurl = "https://fazendanatureza.com/bot/botarz.php?city_name="+city_names+"sector_name="+sector_names
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processlocation(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")
    return city

def processSector(req):
    result = req.get("result")
    parameters = result.get("parameters")
    sector = parameters.get("Location")
    return sector

def makeWebhookResult(data):
    row1_id=data[0]['p_id']
    row1_title = data[0]['title']
    row1_price = data[0]['price']
    row1_location=data[0]['address']
    row1_web_url = data[0]['web_url']
    if row1_title is None:
        return {}
    row2_id=data[1]['p_id']
    row2_title = data[1]['title']
    row2_price = data[1]['price']
    row2_location=data[1]['address']
    row2_web_url = data[1]['web_url']
    # print(json.dumps(item, indent=4))

    speech = "This is the response from server... " +city_name+ "  " +sector_name +"    "+ row1_title +" "+row2_title
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
               "image_url": "https://fazendanatureza.com/bot/house-0.png" ,
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
                "image_url": "https://fazendanatureza.com/bot/house2.png",
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
