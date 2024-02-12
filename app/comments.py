import pandas as pd
from googleapiclient.discovery import build
#importamos las claves de la api
from config.keys import api_service_name, api_version, DEVELOPER_KEY, allowed_fields
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)



def select_fields(link):
    comments = {}
    response = getComment(link)
    #seleccionar solo los campos permitidos
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comment = {key: comment[key] for key in allowed_fields}
        comments[comment['textOriginal']] = comment
    #retornar los comentarios en un dataframe
    return pd.DataFrame.from_dict(comments,orient='index')




def process_item(item):
    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    username = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
    return [username, comment]


def getComment(link, maxResults=100):
    #medir el tiempo de ejecucion
    timeinit = time.time()
    comments = []
    results = youtube.commentThreads().list(
        part='snippet',
        videoId=link,
        textFormat='plainText',
        maxResults=100
    ).execute()

    with ThreadPoolExecutor() as executor:
        while results:
            futures = [executor.submit(process_item, item) for item in results['items']]
            for future in as_completed(futures):
                comments.append(future.result())

            if ('nextPageToken' in results) and (len(comments) <= maxResults):
                nextPage = results['nextPageToken']
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=link,
                    textFormat='plainText',
                    pageToken=nextPage,
                    maxResults=50
                ).execute()
            else:
                break
    #medir el tiempo de ejecucion
    timeend = time.time()
    print('Tiempo de ejecucion obtencion comentarios: ', timeend - timeinit)

    return pd.DataFrame(comments, columns=['authorDisplayName', 'textOriginal'])
#esta funcion solo obtendra 50 comentarios de un video
def getCommentSimple(link):
    #medir el tiempo de ejecucion
    timeinit = time.time()
    comments = []
    results = youtube.commentThreads().list(
        part='snippet',
        videoId=link,
        textFormat='plainText',
        maxResults=50
    ).execute()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_item, item) for item in results['items']]
        for future in as_completed(futures):
            comments.append(future.result())
    #medir el tiempo de ejecucion
    timeend = time.time()
    print('Tiempo de ejecucion obtencion comentarios: ', timeend - timeinit)
    return pd.DataFrame(comments, columns=['authorDisplayName', 'textOriginal'])


