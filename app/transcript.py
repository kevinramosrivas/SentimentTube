import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi




def getTranscript(link):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(link, languages=['es'])
        #retornar la transcripcion del video como un json
        return pd.DataFrame(transcript, columns=['text', 'start', 'duration'])
    except:
        # si el video no tiene transcripcion, retornar un mensaje
        return 'No hay transcripcion para este video'