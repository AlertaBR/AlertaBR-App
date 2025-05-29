import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


class FloodInformations:

    def __init__(self, url, params):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)
        
        self.response = openmeteo.weather_api(url, params=params)
        self.url = url
        self.params = params


    def showLocationInfos(self):
        for i in range(len(self.response)):
            resp = self.response[i]
            print(f"Coordinates {resp.Latitude()}°N {resp.Longitude()}°E")
            print(f"Elevation {resp.Elevation()} m asl")
            print(f"Timezone {resp.Timezone()}{resp.TimezoneAbbreviation()}")
            print(f"Timezone difference to GMT+0 {resp.UtcOffsetSeconds()} s")

    def getHourly(self):
        # Process hourly data. The order of variables needs to be the same as requested.
        return self.response[0].Hourly()


    def createDataFrame(self):
        hourly = self.getHourly()
        
        hourly_rain = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            )
        }

        hourly_data["rain"] = hourly_rain
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["precipitation"] = hourly_precipitation

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        print(hourly_dataframe)



# Código principal
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -23.5475,
    "longitude": -46.6361,
    "hourly": [
        "rain",
        "relative_humidity_2m",
        "weather_code",
        "cloud_cover",
        "precipitation",
    ],
    "timezone": "America/Sao_Paulo",
}

floodObj = FloodInformations(url, params)
floodObj.showLocationInfos()
floodObj.createDataFrame()