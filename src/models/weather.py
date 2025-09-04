import requests
import os
from dotenv import load_dotenv

class Weather():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('WEATHER_API_KEY')
        
    def get(self, city):
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={self.key}&q={city}&aqi=no")
        if response.status_code == 200:
            data = response.json()
            result = {
                "ciudad": city,
                "temperatura": data["current"]["temp_c"],
                "condicion": data["current"]["condition"]["text"],
                "humedad": data["current"]["humidity"],
                "sensacion_termica": data["current"]["feelslike_c"]
            }
            print("Datos del clima obtenidos:", result)
            return result
        else:
            print(f"Error al llamar al API del clima. Código: {response.status_code}")
            return {
                "error": "No se pudo obtener el clima",
                "ciudad": city
            }