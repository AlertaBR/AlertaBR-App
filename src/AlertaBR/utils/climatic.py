import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


class enviromentInfos:

    def __init__(self, latitude, longitude):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession(
            "../cache/cache-openmeteo", expire_after=3600
        )
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)
        self.latitude = latitude
        self.longitude = longitude
        self.response = None

    def showHourlyWeatherInfos(self):
        """Mostra as informações de Enchentes por dia no local ou das previsiões de chuva e humidade

        Args:
            climate (climateTypes, optional): Define qual clima o usuário quer analisar. Defaults to climateTypes.FLOOD.
        """
        self.__getWeatherData()
        self.__showInfos()
    
    def showDailyFloodInfos(self):
        self.__getFloodData()
        self.__showInfos()


    def __showInfos(self):
        for i in range(len(self.response)):
            resp = self.response[i]
            print(f"Coordinates {resp.Latitude()}°N {resp.Longitude()}°E")
            print(f"Elevation {resp.Elevation()} m asl")
            print(f"Timezone {resp.Timezone()}")
    
    def __getDaily(self):
        """Retorna a data do dia a partindo de um response especificado

        Returns:
            VariablesWithTime: Tipo de variável que retorna a data e hora do dado
        """
        return self.response[0].Daily()
    
    def __getHourly(self):
        """Retorna o tempo do dia partindo de um response especificado

        Returns:
            VariablesWithTime: Tipo de variável que retorna a data e hora do dado
        """
        return self.response[0].Hourly()

    def createFloodData(self):
        """
            Cria uma tabela em terminal com as informações da descarga do rio em m³
        """
        self.__getFloodData()
        daily = self.__getDaily()

        daily_river_discharge = daily.Variables(0).ValuesAsNumpy()
        daily_river_discharge_max = daily.Variables(0).ValuesAsNumpy()

        daily_data = {
            "Data": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            ).strftime("%d/%m/%y")
        }

        daily_data["Volume atual do rio"] = daily_river_discharge
        daily_data["Volume máximo atingido"] = daily_river_discharge_max
        
    def createWeatherData(self):
        self.__getWeatherData()
        hourly = self.__getHourly()
        
        hourly_precipitation_probability = hourly.Variables(0).ValuesAsNumpy()
        hourly_rain = hourly.Variables(1).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        ).strftime("%H:%M")}
        
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["rain"] = hourly_rain
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m


    def __getFloodData(self):
        url = "https://flood-api.open-meteo.com/v1/flood"
        params = {
            "latitude": 59.91,
            "longitude": 10.75,
            "daily": ["river_discharge"],
            "models": "seamless_v4",
            "timeformat": "unixtime",
            "forecast_days": 7
        }
        self.response = self.openmeteo.weather_api(url, params)
    
    def __getWeatherData(self):
        # API irá receber os dados por hora dps para fazer um cálculo de prevenção (que não é nossa intenção atual)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["rain", "precipitation", "relative_humidity_2m", "weather_code", "cloud_cover", "showers"],
            "timezone": "auto",
            "timeformat": "unixtime",
            "forecast_days": 1
        }
        self.response = self.openmeteo.weather_api(url, params)
    

# Código principal