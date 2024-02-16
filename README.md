# SentimentTube

Esta es una aplicación Flask que proporciona endpoints para analizar la emoción y el sentimiento de transcripciones de videos de YouTube y comentarios asociados a esos videos.

## Configuración

Puedes instalar las dependencias de la aplicación utilizando `pip` y el archivo `requirements.txt` proporcionado:

```
pip install -r requirements.txt
```

## Uso

Para ejecutar la aplicación, simplemente ejecuta el archivo `application.py`. Esto iniciará un servidor web local que escucha en el puerto 105 por defecto.

```bash
python run.py
```

## Endpoints

### 1. `/getEmotionTranscript/<link>`

Este endpoint recibe un enlace a un video de YouTube y devuelve la transcripción del video junto con la distribución de emociones detectadas en la transcripción.

#### Método: `GET`

Parámetros:
- `link`: identificador del video de YouTube.

Ejemplo de uso:
```
GET http://127.0.0.1:105/getEmotionTranscript/jSaSZ8omve0
```

### 2. `/getSentimentComments/?link=<link>&maxResults=<maxResults>`

Este endpoint recibe un enlace a un video de YouTube y opcionalmente el número máximo de comentarios a analizar, y devuelve los comentarios junto con la distribución de sentimientos detectados en los comentarios.

#### Método: `GET`

Parámetros:
- `link`: identificador del video de YouTube.
- `maxResults` (opcional): Número máximo de comentarios a analizar. Por defecto, se analizan 50 comentarios.

Ejemplo de uso:
```
GET http://127.0.0.1:105/getSentimentComments/?link=jSaSZ8omve0&maxResults=100
```

## Créditos

Esta aplicación fue desarrollada por G3 en el curso de Taller de aplicaciones sociales - UNMSM 2024-0.
