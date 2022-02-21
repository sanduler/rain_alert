# Name: Ruben Sanduleac
#
import requests
import os
from twilio.rest import Client


# API_KEY = "PLACE_API_KEY_HERE"
API_KEY = ""
account_sid = os.environ['TWILIO_ACCOUNT_SID'] = ""
auth_token = os.environ['TWILIO_AUTH_TOKEN'] = ""
FROM_PHONE = ""
TO_PHONE = ""
WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
CURRENT_LAT = 45.523064
CURRENT_LON = -122.676483

parameters = {
    "lat": CURRENT_LAT,
    "lon": CURRENT_LON,
    "appid": API_KEY,
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(url=WEATHER_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
condition_code: int

weather_slice = data["hourly"][:12]
bring_umbrella = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        bring_umbrella = True

if bring_umbrella:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today! Don't forget to bring an Umbrella ☂️ ☂",
        from_=FROM_PHONE,
        to=TO_PHONE
    )

print(message.status)