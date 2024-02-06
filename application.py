from concurrent.futures import ThreadPoolExecutor
from flask import Flask
import pandas as pd
from app.comments import select_fields
from app.transcript import getTranscript
from app.preprocess import preprocess_comments, preprocess_transcript
from app.sentiment_analysis import get_sentiment
from app.emotion_analysis import get_emotion
import json
#importar jsonify
from flask import jsonify
def process_comments(link):
    comments = select_fields(link)
    comments = preprocess_comments(comments)
    comments, distribution_comments = get_sentiment(comments)
    return comments, distribution_comments

def process_transcript(link):
    transcript = getTranscript(link)
    transcript = preprocess_transcript(transcript)
    transcript, distribution_transcript = get_emotion(transcript)
    return transcript, distribution_transcript

def create_app():
    app = Flask(__name__)
    # will move to register_config soon
    app.config['ERROR_404_HELP'] = False

    # crear las rutas de la aplicacion
    # pasar un link al end point getText para que lo analice
    @app.route('/getText/<link>', methods=['GET'])
    @app.route('/', methods=['GET'])
    def getText(link=None):
        with ThreadPoolExecutor() as executor:
            # Ejecutar process_comments y process_transcript en hilos separados
            comments_future = executor.submit(process_comments, link)
            transcript_future = executor.submit(process_transcript, link)

            # Obtener los resultados de los hilos
            comments, comments_distribution = comments_future.result()
            transcript , transcript_distribution = transcript_future.result()

            #guardar los resultados en un csv
            comments.to_csv('data_csv/comments.csv')
            transcript.to_csv('data_csv/transcript.csv')
        #devolver las distribuciones de sentimientos y emociones
        return jsonify({
            'comments':  comments_distribution,
            'transcript': transcript_distribution
        })

    return app
