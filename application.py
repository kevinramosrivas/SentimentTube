from flask import Flask
import pandas as pd
from app.comments import select_fields
from app.transcript import getTranscript
from app.preprocess import preprocess_comments, preprocess_transcript
from app.sentiment_analysis import get_sentiment
import json

def create_app():
    app = Flask(__name__)
    # will move to register_config soon
    app.config['ERROR_404_HELP'] = False
        # crear las rutas de la aplicacion
    #pasar un link al end point getText para que lo analice
    @app.route('/getText/<link>', methods=['GET'])
    @app.route('/', methods=['GET'])
    def getText(link=None):
        #AÑADIR AL JSON DE COMENTARIOS LA TRANSCRIPCION DEL VIDEO
        comments = select_fields(link)
        transcript = getTranscript(link)
        comments = preprocess_comments(comments)
        transcript = preprocess_transcript(transcript)
        comments = get_sentiment(comments)
        transcript = get_sentiment(transcript)
        comments.to_csv('data_csv/comments.csv',index = False)
        transcript.to_csv('data_csv/transcript.csv',index = False)
        return 'ok'
    
    return app