
# Asistente virtual

## Configuración
Para ejecutar el proyecto es necesario:
1. Descargar el repositorio

2. Configurar el entorno Python:
   - Recomendado: Crear un ambiente virtual:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate  # En Windows
     source .venv/bin/activate  # En Linux/Mac
     ```

3. Instalar herramientas base (importante para evitar errores):
   ```bash
   python -m pip install --upgrade pip
   pip install wheel setuptools
   ```

4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   
   Si encuentras errores con paquetes como `frozenlist`, `multidict`, `yarl` o `aiohttp`, instálalos individualmente:
   ```bash
   pip install frozenlist multidict yarl aiohttp
   ```
   
5. Crear un archivo `.env` con las siguientes claves:
   ```
   NOVITA_API_KEY=XXXXXX      # API key de Novita AI
   ELEVENLABS_API_KEY=XXXXXX  # API key de ElevenLabs para TTS
   WEATHER_API_KEY=XXXXXX     # API key para el servicio del clima
   ```

### Requisitos del Sistema
- Python 3.8 o superior
- En Windows: 
  - Visual C++ 14.0 o superior (necesario para algunas dependencias)
  - Puedes instalarlo con "Build Tools for Visual Studio"


## Ejecución
- Este proyecto utiliza Flask. Puedes levantar el servidor en modo debug por defecto en el puerto 5000 con el comando
	- ```flask --app app run --debug```
	- En tu navegador ve a http://localhost:5000
	- Da clic para comenzar a grabar (pedirá permiso). Dar clic para dejar de grabar


## Licencias
- Imagen de micrófono por Freepik
- Parte del código Este repositorio es el código para el video del Asistente Virtual en el canal Ringa Tech:
https://youtu.be/-0tIy8wWtzE