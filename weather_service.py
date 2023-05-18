from flask import Flask
from flask import request
import requests
import json
import flask


app = Flask(__name__)
app.config.from_pyfile('settings.py')


@app.route('/forecast_weather', methods=['GET'])
def get():
    city = request.args.get('city')
    dt = request.args.get('dt')
    #url = 'http://api.weatherapi.com/v1/forecast.json?key=92b2b54828074632897211731232702&q={}&days=14'
    url = app.config.get("URL")
    url = url.format(city)
    data = requests.get(url).content
    data = json.loads(data.decode('utf-8'))
    print(type(data))
    if len(dt.split("_")) == 2:
        dt = dt.replace("_", " ")
        for date in data["forecast"]["forecastday"]:
            for dtime in date["hour"]:
                print(dtime)
                print(str(dt))
                if str(dtime["time"]) == str(dt):
                    print("da2")
                    resp_date = str(dtime["temp_c"])
    elif len(dt.split("_")) == 1:
        for date in data["forecast"]["forecastday"]:
            if date["date"] == dt:
                print(date["hour"][1])
                resp_date = str(date["day"]["avgtemp_c"])

    print(resp_date)
    resp = {"city": data["location"]["name"], "unit": "celsius", "temperature": resp_date}

    return flask.jsonify(resp)


@app.route('/current_weather', methods=['GET'])
def cur():
    city = request.args.get('city')
    #url = 'http://api.weatherapi.com/v1/forecast.json?key=92b2b54828074632897211731232702&q={}&days=14'
    print("da, zashel")
    url = app.config.get("URL")
    url = url.format(city)
    data = requests.get(url).content
    data = json.loads(data.decode('utf-8'))
    #print(app.config.get("URL"))
    resp = {"city": data["location"]["name"], "unit": "celsius","temperature": data["current"]["temp_c"]}

    return flask.jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)
