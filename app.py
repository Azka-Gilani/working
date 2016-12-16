#!/usr/bin/env python

import urllib
import urllib2
import json
import os
import re


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
intent_name="string"
QR=['0','1','2','3','4','5','6']

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
    global QR
    global intent_name
    intent_name=processIntentName(req)
    if "ChooseCity" in intent_name:        
        QR[0]="Sector in "+city_names
        QR[1]="Other City?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type"
    elif "ChooseSector" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Sector?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Property Type"   
    elif "ChangeType" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Type?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"  
    elif "ChooseHotProperties" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Change Location"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change City" 
    elif "ChoosePlotArea" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Area?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"
    elif "DefinePriceRange" in intent_name:        
        QR[0]="(Y)"
        QR[1]="Other Range?Specify"
        QR[2]="Hot Property"
        QR[3]="Price Range"
        QR[4]="Land Area"
        QR[5]="Change Location"
    city_names=processlocation(req)
    sector_names=processSector(req)
    property_type=processPropertyType(req)
    unit_property=processUnit(req)
    area_property=processArea(req)
    NoOfDays=processDate(req)
    DateUnit=processDateUnit(req)
    school=processSchool(req)
    malls=processMalls(req)
    transport=processTransport(req)
    security=processSecurity(req)
    airport=processAirport(req)
    fuel=processFuel(req)
    #minimum_value=processMinimum(req)
    maximum_value=processMaximum(req)
    latest=processLatestProperties(req)
    #if minimum_value > maximum_value:
    #    minimum_value,maximum_value=maximum_value,minimum_value
    #else:
    # minimum_value,maximum_value=minimum_value,maximum_value    
    baseurl = "https://aarz.pk/bot/index.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def processIntentName(req):
    result = req.get("result")
    parameters = result.get("metadata")
    intent = parameters.get("intentName")
    return intent

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

def processMinimum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    minimum = parameters.get("number")
    return minimum

def processMaximum(req):
    result = req.get("result")
    parameters = result.get("parameters")
    maximum = parameters.get("number1")
    return maximum


def processPropertyType(req):
    result = req.get("result")
    parameters = result.get("parameters")
    propertyType = parameters.get("PropertyType")
    return propertyType

def processLatestProperties(req):
    result = req.get("result")
    parameters = result.get("parameters")
    latest = parameters.get("LatestProperties")
    return latest

def processUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    unit = parameters.get("Unit")
    return unit

def processArea(req):
    result = req.get("result")
    parameters = result.get("parameters")
    area = parameters.get("AreaNumber")
    return area

def processDate(req):
    result = req.get("result")
    parameters = result.get("parameters")
    days = parameters.get("NoOfDays")
    return days

def processDateUnit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    dayUnit = parameters.get("DayUnit")
    return dayUnit

def processSchool(req):
    result = req.get("result")
    parameters = result.get("parameters")
    school = parameters.get("school")
    return school

def processMalls(req):
    result = req.get("result")
    parameters = result.get("parameters")
    malls = parameters.get("malls")
    return malls

def processTransport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    transport = parameters.get("transport")
    return transport

def processSecurity(req):
    result = req.get("result")
    parameters = result.get("parameters")
    security = parameters.get("security")
    return security

def processAirport(req):
    result = req.get("result")
    parameters = result.get("parameters")
    airport = parameters.get("airport")
    return airport

def processFuel(req):
    result = req.get("result")
    parameters = result.get("parameters")
    fuel = parameters.get("fuelstation")
    return fuel

def makeWebhookResult(data):
    i=0
    length=len(data)
    row_id=['test','test1','test2']
    row_title=['test','test1','test2']
    row_location=['test','test1','test2']
    row_price=['test','test1','test2']
    row_slug=['test','test1','test2']
    while (i <length):
        row_id[i]=data[i]['p_id']
        row_title[i]=data[i]['title']
        row_location[i]=data[i]['address']
        row_price[i]=data[i]['price']
        row_slug[i]=data[i]['slug']
        i+=1
        
    speech = "Here are some properties with your choice: "+"\n"+row_title[0] +" in "+ row_location[0] + " with price "+ row_price[0] +"\n"+ row_title[1] +" in "+ row_location[1] + " with price "+ row_price[1]
    print("Response:")
    print(speech)
    if "unable" in row_title[0]:
        message={
         "text":row_title[0],
         "quick_replies": [
           
                 {
                "content_type":"text",
                "title": "Purchase plot",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
           
    }
    elif length==1:
                 message={
                   "attachment":{
                    "type":"template",
                       "payload":{
            "template_type":"generic",
            "elements":[
          {
             "title":row_title[0],
             "item_url":"http://www.aarz.pk/property-detail/"+row_slug[0],
             "image_url":"http://www.aarz.pk/assets/images/properties/"+row_id[0]+"/"+row_id[0]+".actual.0.jpg",
             "subtitle":row_location[0],
             "buttons":[
              {
               "type":"web_url",
               "url": "https://www.aarz.pk/property-detail/"+row_slug[0],  
               "title":"View Website"
              }, 
                {
                "type":"element_share"
                  } 
            ]
          }
        ]
      }
    },
                      "quick_replies": [
            {
                "content_type":"text",
                "title": QR[0],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[1],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[2],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[3],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[4],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": "Purchase Property",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
  }
    else:
        message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row_title[0],
               "subtitle": row_location[0],
               "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"http://www.aarz.pk/assets/images/properties/"+row_id[0]+"/"+row_id[0]+".actual.0.jpg" ,
                "buttons": [{
                "type": "web_url",
                "url":  "https://www.aarz.pk/property-detail/"+row_slug[0],  
                "title": "Open Web URL"
            }, 
                 {
                "type":"element_share"
                  }   
                   ]
                   
                           
              
          }, 
                   {
                "title": row_title[1],
                "subtitle": row_location[1],
                "item_url":   "https://www.aarz.pk/property-detail/"+row_slug[1],             
                "image_url": "http://www.aarz.pk/assets/images/properties/"+row_id[1]+"/"+row_id[1]+".actual.0.jpg",
                "buttons": [{
                "type": "web_url",
                "url":  "https://www.aarz.pk/property-detail/"+row_slug[1],  
                "title": "Open Web URL"
            },
                {
                "type":"element_share"
                  } 
                   ]
          }]
            
        }
      },
             "quick_replies": [
            {
                "content_type":"text",
                "title": QR[0],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[1],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[2],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[3],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": QR[4],
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            },
                 {
                "content_type":"text",
                "title": "Purchase Property",
                "payload": "YOUR_DEFINED_PAYLOAD_FOR_NEXT_IMAGE"
            }
        ]
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
