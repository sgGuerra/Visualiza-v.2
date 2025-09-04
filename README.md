# Visualiza - Asistente Virtual

Proyecto para un asistente virtual diseñado para personas ciegas.

## Instalación

1. Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el servidor Flask:

```bash
python app.py
```

El servidor se ejecutará en `http://localhost:5000/`.

## Manejo de errores

- Asegúrate de tener las variables de entorno configuradas en un archivo `.env`.
- Si el servidor no inicia, revisa que no haya otro proceso usando el puerto 5000.
- Para problemas con dependencias, verifica que todas estén instaladas correctamente con la versión adecuada.
- Los errores de grabación de audio pueden deberse a permisos del navegador o falta de HTTPS.

## Dependencias

Las dependencias principales están listadas en `requirements.txt`. Asegúrate de instalar todas antes de ejecutar la aplicación.

## Testing

- Se incluyen pruebas unitarias para servicios y rutas principales.
- Ejecuta las pruebas con:

```bash
pytest
```

## Contacto

Para soporte o preguntas, contacta al equipo de desarrollo.
