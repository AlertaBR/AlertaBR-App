import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from src.AlertaBR.logic.verifications import ConvertUnix


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
   
    def __getDaily(self):
        """Retorna a data do dia a partindo de um response especificado

        Returns:
            VariablesWithTime: Tipo de variável que retorna a data e hora do dado
        """
        return self.response[0].Daily()
    
    def __getCurrent(self):
        """Retorna o tempo do dia partindo de um response especificado

        Returns:
            VariablesWithTime: Tipo de variável que retorna a data e hora do dado
        """
        return self.response[0].Current()

    def createFloodData(self):
        """
            Cria uma tabela em terminal com as informações da descarga do rio em m³
        """
        self.__getFloodData()
        daily = self.__getDaily()

        daily_river_discharge = daily.Variables(0).ValuesAsNumpy()

        flood_data = {
            "date": pd.date_range(
                    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
                    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
                    freq = pd.Timedelta(seconds = daily.Interval()),
                    inclusive = "left").strftime("%d/%m/%y"),
            "river_discharge": daily_river_discharge,
        }
        
        # for i in range(7):
        #     for key in daily_data.keys():
        #         print(f'{key}: {daily_data[key][i]}')
        #     print()
        return flood_data
        
        
        
    def createWeatherData(self):
        """
            Cria uma tabela em terminal com a previsão de chuva dos próximos dias 
        """
        weatherInfos = {}
        
        self.__getWeatherData()
        current = self.__getCurrent()
        daily = self.__getDaily()
        
        weatherInfos['rain'] = current.Variables(0).Value()
        weatherInfos['rainSum'] = daily.Variables(0).ValuesAsNumpy()
        weatherInfos['precipitation_probability'] = current.Variables(1).Value()
        weatherInfos['relative_humidity'] = current.Variables(2).Value()
        weatherInfos['weather_code'] = current.Variables(3).Value()
        weatherInfos['showers'] = current.Variables(4).Value()
        weatherInfos['showersSum'] = daily.Variables(1).ValuesAsNumpy()

        # print(f"Current time {ConvertUnix(current.Time())}")
        # for k,v in currentWeather.items():
        #     print(f'{k} atual: {v}')
        return weatherInfos


    def __getFloodData(self):
        url = "https://flood-api.open-meteo.com/v1/flood"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "daily": ["river_discharge_median"],
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
            "daily": ["rain_sum", "showers_sum"],
            "current": ["precipitation", "precipitation_probability", "relative_humidity_2m", "weather_code", "showers"],
            "timezone": "auto",
            "forecast_days": 7
        }
        self.response = self.openmeteo.weather_api(url, params)