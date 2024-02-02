import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi




def getTranscript(link):
    textTranscript = []
    try:
        transcript = YouTubeTranscriptApi.get_transcript(link, languages=['es'])
        for item in transcript:
            textTranscript.append(item['text'])
        #retornar la transcripcion del video como un json
        return pd.DataFrame(textTranscript, columns=['text'])
    except:
        # si el video no tiene transcripcion, retornar un mensaje
        return 'No hay transcripcion para este video'