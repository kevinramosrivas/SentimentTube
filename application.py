from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request
import pandas as pd
from app.comments import select_fields, getComment
from app.transcript import getTranscript
from app.preprocess import preprocess_comments, preprocess_transcript
from app.sentiment_analysis import get_sentiment
from app.emotion_analysis import get_emotion
import json
#importar jsonify
from flask import jsonify


def create_app():
    app = Flask(__name__)
    # will move to register_config soon
    app.config['ERROR_404_HELP'] = False

    # crear las rutas de la aplicacion
    # pasar un link al end point getText para que lo analice
    @app.route('/getEmotionTranscript/<link>', methods=['GET'])
    def getText(link=None):
        transcript = getTranscript(link)
        transcript = preprocess_transcript(transcript)
        transcript, distribution_transcript = get_emotion(transcript)
        return jsonify(distribution_transcript)
    
    # pasar oos parametros al end point getSentimentComments para que lo analice, se debe pasar un link y un maxResults
    @app.route('/getSentimentComments/', methods=['GET'])
    def getSentimentComments():
        link = request.args.get('link')
        #maxResults debe ser un numero entero
        maxResults = request.args.get('maxResults')
        if maxResults is None:
            maxResults = 100
        #convertir maxResults a entero
        maxResults = int(maxResults)
        comments = getComment(link, maxResults=maxResults)
        comments = preprocess_comments(comments)
        comments, distribution_comments = get_sentiment(comments)
        return jsonify(distribution_comments)

    return app
