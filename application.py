from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request
import pandas as pd
from app.comments import select_fields, getComment, getCommentSimple
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
    # este end point puede ser accedido por ejemplo desde http://127.0.0.1:105/getEmotionTranscript/jSaSZ8omve0
    @app.route('/getEmotionTranscript/<link>', methods=['GET'])
    def getEmotionTranscript(link=None):
        transcript = getTranscript(link)
        preproces_transcript = preprocess_transcript(transcript)
        transcript, distribution_transcript = get_emotion(preproces_transcript)
        return jsonify(
            {
                'distribution_transcript': distribution_transcript,
                'transcript': transcript
            }
        )
    
    # pasar oos parametros al end point getSentimentComments para que lo analice, se debe pasar un link y un maxResults
    # este ebd point puede ser accedido por ejemplo desde http://127.0.0.1:105/getSentimentComments/?link=jSaSZ8omve0&maxResults=100
    #donde maxResults es el numero de comentarios a analizar y es opcional
    @app.route('/getSentimentComments/', methods=['GET'])
    def getSentimentComments():
        link = request.args.get('link')
        #maxResults debe ser un numero entero
        maxResults = request.args.get('maxResults')
        #convertir maxResults a entero si es que no es nulo
        if maxResults!=None:
            maxResults = int(maxResults)
        else:
            maxResults = 50
        comments = getComment(link, maxResults)
        comments = preprocess_comments(comments)
        comments, distribution_comments, words_count = get_sentiment(comments)
        return jsonify({
            'distribution_comments': distribution_comments,
            'comments': comments,
            'words': words_count
        })
        

    return app
