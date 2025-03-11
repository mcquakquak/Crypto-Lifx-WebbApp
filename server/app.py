from types import MethodType
from typing import TYPE_CHECKING
from flask import Flask, request
import requests
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.route('/', methods=['GET'])
def index():
    return json.dumps({"": 'Hello, THIS IS BOB.'})


def getMarketData(coin):
    headers = {"Authorization": "Bearer CG-D7S4yMDC6zeMGn1SXLAzctjg"}
    response = requests.get('https://api.coingecko.com/api/v3/simple/price',
                            params={
                                "ids": coin,
                                "vs_currencies": "usd",
                                "include_24hr_change": "true",
                                "precision": "4"
                            },
                            headers=headers)

    response = response.json()

    #TODO Create proper error handling incase the coin doesnt exist

    return {"24_hour_change": response[coin]["usd_24h_change"]}


def changeLightClr(dayChange):

    if dayChange > 0:
        lightClr = "green"
    elif dayChange < 0:
        lightClr = "red"
    elif dayChange == 0:
        lightClr = "yellow"
    else:
        lightClr = "blue"

    return lightClr


def setLightColor(lightClr):
    headers = {
        "Authorization":
        "Bearer c98101b4cca628009dd161a8bb16fc438fa4641b59fc6ef8d057d20bc20993b7"
    }
    response = requests.put('https://api.lifx.com/v1/lights/all/state',
                            params={
                                "duration": 1,
                                "fast": False,
                                "power": "on",
                                "color": lightClr,
                                "brightness": 1
                            },
                            headers=headers)

    print(response.json())


@app.route('/change_light/<coin>', methods=['POST'])
def main(coin):
    dayChange = getMarketData(coin)
    lightClr = changeLightClr(dayChange["24_hour_change"])
    setLightColor(lightClr)
    return {
        "dayChange":
        dayChange["24_hour_change"],
        "friendlyMessage":
        "The function above worked, hurray, it returned the 24 hour change of "
        + coin,
        "status":
        200,
        "expectedLightColor":
        lightClr
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)