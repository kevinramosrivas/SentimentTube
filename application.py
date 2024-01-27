from flask import Flask
import pandas as pd
from app.comments import select_fields
from app.transcript import getTranscript


def create_app():
    app = Flask(__name__)
    # will move to register_config soon
    app.config['ERROR_404_HELP'] = False
        # crear las rutas de la aplicacion
    #pasar un link al end point getSentiment para que lo analice
    @app.route('/getSentiment/<link>', methods=['GET'])
    @app.route('/', methods=['GET'])
    def getSentiment(link):
        #AÑADIR AL JSON DE COMENTARIOS LA TRANSCRIPCION DEL VIDEO
        comments = select_fields(link)
        transcript = getTranscript(link)

        #guardar los comentarios en un csv
        comments.to_csv('comments.csv', index=False)
        #guardar la transcripcion en un csv
        transcript.to_csv('transcript.csv', index=False)
        return 'ok'
    return app