from flask import Flask
import googleapiclient.discovery
import pandas as pd
from flask import jsonify
from youtube_transcript_api import YouTubeTranscriptApi


api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAjmVjeBSSpx7ISnuFMRfPUSDmaLDdsEfY"
allowed_fields = ['authorDisplayName', 'publishedAt', 'likeCount', 'textOriginal']

app = Flask(__name__)


#pasar un link al end point getSentiment para que lo analice
@app.route('/getSentiment/<link>', methods=['GET'])
def getSentiment(link):
    video = {}
    #AÑADIR AL JSON DE COMENTARIOS LA TRANSCRIPCION DEL VIDEO
    comments = select_fields(link)
    transcript = getTranscript(link)

    #unir los comentarios y la transcripcion en un solo json
    video = {
        'comments': comments,
        'transcript': transcript
    }
    return jsonify(video)


def select_fields(link):
    comments = {}
    response = getComment(link)
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.update({
            comment['authorDisplayName']: {
                'publishedAt': comment['publishedAt'],
                'likeCount': comment['likeCount'],
                'textOriginal': comment['textOriginal']
            }
        })
    #retornar el diccionario de comentarios
    return comments
    

def getComment(link):
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=link,
        maxResults=100
    )

    # Execute the request.
    return request.execute()

def getTranscript(link):
    textTranscript = []
    transcript = YouTubeTranscriptApi.get_transcript(link, languages=['es'])
    for item in transcript:
        textTranscript.append(item['text'])
    return textTranscript


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=105, debug=True)