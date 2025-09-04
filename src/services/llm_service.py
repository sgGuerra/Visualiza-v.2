from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class LLM():
    def __init__(self):
        # Configuración de Novita AI
        self.base_url = "https://api.novita.ai/openai"
        self.api_key = os.getenv('NOVITA_API_KEY')
        # Puedes cambiar el modelo según tus necesidades:
        # - meta-llama/llama-3.1-8b-instruct
        # - openchat/openchat-3.5-1210
        # - codellama/codellama-34b-instruct
        # - anthropic/claude-2.1
        self.model = "meta-llama/llama-3.1-8b-instruct"
        
        # Inicializar cliente
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
    
    def process_functions(self, text):
        # Lista de funciones disponibles para el prompt
        functions_description = """
        Funciones disponibles:
        1. get_weather(ubicacion: string) - Obtener el clima actual de una ciudad
           - Se debe usar cuando el usuario pregunte sobre el clima, temperatura o condiciones meteorológicas
           - Ejemplos de preguntas que activan esta función:
             * "¿Cómo está el clima en [ciudad]?"
             * "¿Qué temperatura hace en [ciudad]?"
             * "Clima en [ciudad]"
             * "¿Está lloviendo en [ciudad]?"
             * "¿Qué tiempo hace en [ciudad]?"
           - Responder con: {"function": "get_weather", "args": {"ubicacion": "nombre_ciudad"}}

        2. send_email(recipient: string, subject: string, body: string) - Enviar un correo
        3. open_browser(website: string) - Abrir un navegador web en un sitio específico
        4. play_on_youtube(song: string) - Reproducir una canción en YouTube

        IMPORTANTE: Cualquier pregunta sobre clima, temperatura o condiciones meteorológicas DEBE usar la función get_weather.
        Para reproducir música en YouTube, usa la función play_on_youtube con el nombre de la canción.
        Responde SIEMPRE con un JSON en este formato exacto:
        {"function": "nombre_funcion", "args": {"argumento1": "valor1"}}

        Para el clima, extrae la ciudad mencionada y úsala como ubicación.
        Si no está relacionado con ninguna función, responde normalmente.
        """
        
        # Primero, analicemos si es una consulta de clima
        is_weather_query = any(keyword in text.lower() for keyword in [
            "clima", "temperatura", "tiempo hace", "lluvia", "lloviendo",
            "calor", "frío", "como esta el", "que tal esta"
        ])

        # Analizar si es una solicitud para reproducir música en YouTube
        music_keywords = ["reproduce en youtube", "reproducir en youtube", "pon musica en youtube", "pon música en youtube"]
        is_music_query = any(keyword in text.lower() for keyword in music_keywords)

        system_prompt = """Eres un asistente personal diseñado para apoyar de forma empática, clara y eficiente a una persona ciega en sus actividades diarias. Tu objetivo es facilitar la autonomía, brindar información útil y orientar con precisión, utilizando únicamente referencias que sean accesibles a través del tacto, el sonido, el olfato, la memoria, la ubicación espacial y el contexto funcional.

Todas tus respuestas deben ser prácticas, descriptivas desde una perspectiva no visual y adaptadas a la experiencia sensorial de una persona ciega. Evita por completo mencionar colores, apariencias visuales, expresiones faciales o cualquier detalle que dependa de la vista.

Prioriza:
- Orientación espacial clara usando referencias táctiles y sonoras
- Descripciones funcionales de objetos
- Instrucciones paso a paso
- Identificación de sonidos ambientales relevantes
- Apoyo emocional con tono respetuoso y empático
"""

        # Si es una consulta de clima, añadimos instrucciones específicas
        if is_weather_query:
            system_prompt += """
IMPORTANTE - DETECCIÓN DE CONSULTAS DE CLIMA:
Has detectado una consulta sobre el clima. DEBES responder con un JSON en este formato:
{"function": "get_weather", "args": {"ubicacion": "CIUDAD_MENCIONADA"}}

Por ejemplo, si preguntan "clima en Medellín", responde:
{"function": "get_weather", "args": {"ubicacion": "Medellin"}}
"""

        # Si es una consulta para reproducir música en YouTube, añadimos instrucciones específicas
        if is_music_query:
            system_prompt += """
IMPORTANTE - DETECCIÓN DE CONSULTAS DE MÚSICA EN YOUTUBE:
Has detectado una consulta para reproducir música en YouTube. DEBES responder con un JSON en este formato:
{"function": "play_on_youtube", "args": {"song": "NOMBRE_DE_LA_CANCION"}}

Por ejemplo, si preguntan "reproduce en youtube Despacito", responde:
{"function": "play_on_youtube", "args": {"song": "Despacito"}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt + functions_description},
                {"role": "user", "content": text},
            ],
            response_format={"type": "text"}  # Asegurar respuesta en texto para Novita
        )
        
        message = response.choices[0].message
        
        try:
            # Intentar parsear la respuesta como JSON
            response_text = message.content.strip()
            if response_text.startswith('{') and response_text.endswith('}'):
                response_json = json.loads(response_text)
                if 'function' in response_json and 'args' in response_json:
                    return response_json['function'], response_json['args'], message
        except json.JSONDecodeError:
            pass
        
        return None, None, message
    
    #Una vez que llamamos a la funcion (e.g. obtener clima, encender luz, etc)
    #Podemos llamar a esta funcion con el msj original, la funcion llamada y su
    #respuesta, para obtener una respuesta en lenguaje natural (en caso que la
    #respuesta haya sido JSON por ejemplo
    def process_response(self, text, message, function_name, function_response):
        if function_name == "open_browser":
            # Para abrir navegador, generar respuesta confirmando la acción
            website = function_response.get('website', 'la página')
            prompt_system = f"""Eres un asistente personal. El usuario pidió abrir una página web. Genera una respuesta natural y confirmatoria que incluya:
            1. Confirmar que se abrió la página
            2. Mencionar el nombre de la página o sitio
            3. Si hay instrucciones adicionales (como reproducir música), incluirlas en la confirmación
            4. Mantener un tono amigable y útil

            Ejemplo: Si el usuario dice "abre youtube y reproduce y siempre de karolina", responde algo como "Listo, ya abrí YouTube y comenzaré a reproducir 'Y siempre de Karolina' para que suene la canción."

            La página a abrir es: {website}
            """
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": text},
                    {"role": "assistant", "content": message.content},
                    {"role": "system", "content": "Genera una respuesta natural confirmando la apertura de la página."}
                ],
                response_format={"type": "text"}
            )
            return response.choices[0].message.content
        elif function_name == "play_on_youtube":
            # Para reproducir música en YouTube, generar respuesta confirmando la acción
            song = function_response.get('song', 'la canción')
            prompt_system = f"""Eres un asistente personal. El usuario pidió reproducir una canción en YouTube. Genera una respuesta natural y confirmatoria que incluya:
            1. Confirmar que se está reproduciendo la canción
            2. Mencionar el nombre de la canción
            3. Mantener un tono amigable y útil

            Ejemplo: Si el usuario dice "reproduce en youtube Despacito", responde algo como "Listo, ya estoy reproduciendo 'Despacito' en YouTube para que suene la canción."

            La canción a reproducir es: {song}
            """
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": text},
                    {"role": "assistant", "content": message.content},
                    {"role": "system", "content": "Genera una respuesta natural confirmando la reproducción de la canción."}
                ],
                response_format={"type": "text"}
            )
            return response.choices[0].message.content
        else:
            # Para otras funciones como clima
            prompt_system = """Eres un asistente personal para personas ciegas. Al informar sobre el clima, debes:
            1. Extraer la temperatura, condición, humedad y sensación térmica del JSON
            2. Proporcionar información relevante para la planificación táctil y auditiva:
               - Sugerir el tipo de ropa adecuada según la temperatura
               - Mencionar si se necesita paraguas o impermeable
               - Advertir sobre condiciones que afecten la orientación (viento fuerte, lluvia)
               - Indicar si hay riesgos específicos (suelo resbaladizo, charcos)
            3. Incluir información sobre:
               - Sonidos ambientales esperados (lluvia, viento, truenos)
               - Sensaciones térmicas y de humedad relevantes
            4. Dar recomendaciones prácticas para la movilidad y protección

            Ejemplo de respuesta:
            "En [ciudad] la temperatura es de [temperatura]°C, se siente como [sensacion_termica]°C. Hay [condicion], así que escucharás [sonidos_relevantes]. Te recomiendo llevar [tipo_ropa] y [equipamiento_necesario]. Ten en cuenta que [advertencias_movilidad]."
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": text},
                    {"role": "assistant", "content": message.content},
                    {"role": "system", "content": "El servicio del clima retornó este JSON:"},
                    {"role": "system", "content": function_response},
                    {"role": "system", "content": "Genera una respuesta natural incluyendo la información del clima."}
                ],
                response_format={"type": "text"}  # Asegurar respuesta en texto para Novita
            )
            return response.choices[0].message.content
