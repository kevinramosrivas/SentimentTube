import pandas as pd
import googleapiclient.discovery
#importamos las claves de la api
from config.keys import api_service_name, api_version, DEVELOPER_KEY, allowed_fields



def select_fields(link):
    comments = {}
    response = getComment(link)
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        #seleccionar los campos que se van a guardar
        comment = {field: comment[field] for field in allowed_fields}
        comments[comment['textOriginal']] = comment
    #retornar los comentarios en un dataframe
    return pd.DataFrame.from_dict(comments, orient='index')
    
    

def getComment(link):
    comments = {}
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=link,
        maxResults=100
    )
    comments = request.execute()
    while 'nextPageToken' in comments:
        nextPage = youtube.commentThreads().list(
            part="snippet",
            videoId=link,
            maxResults=100,
            pageToken=comments['nextPageToken']
        )
        comments['items'] = comments['items'] + nextPage.execute()['items']
        if 'nextPageToken' not in nextPage.execute():
            break
        comments['nextPageToken'] = nextPage.execute()['nextPageToken']
        #detener si hay mas de 500 comentarios
        if len(comments['items']) > 500:
            break
    return comments