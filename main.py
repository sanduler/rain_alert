# Name: Ruben Sanduleac
#
import requests
import os
from twilio.rest import Client


# the API Keys and Phone numbers hidden in env variables
OPEN_WEATHER_API_KEY = os.environ["OPEN_WEATHER_API"]
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
FROM_PHONE = os.environ["FROM_TEXT"]
TO_PHONE = os.environ["TO_TEXT"]

# openweather endpoint
WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
# location for the weather
CURRENT_LAT = 45.523064
CURRENT_LON = -122.676483

# pull the needed parameters from openweather
parameters = {
    "lat": CURRENT_LAT,
    "lon": CURRENT_LON,
    "appid": OPEN_WEATHER_API_KEY,
    "exclude": "current,minutely,daily,alerts"
}

# get a response from OpenWeather
response = requests.get(url=WEATHER_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()

# preset the conditional to int
condition_code: int

# continue only for 12hrs starting at 7am (7am - 7pm)
weather_slice = data["hourly"][:12]
# bool tag do we need an ubreala? No
bring_umbrella = False
# check each hour if the weathe code matches the condition
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    # anything less than 700 will be rain anothing above is snow or fog
    if condition_code < 700:
        bring_umbrella = True

# twilio API implementation send a text automaticly if it will rain
if bring_umbrella:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today! Don't forget to bring an Umbrella ☂️ ☂",
        from_=FROM_PHONE,
        to=TO_PHONE
    )

# print the status once the text is sent.
print(message.status)