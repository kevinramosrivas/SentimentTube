import pandas as pd
from googleapiclient.discovery import build
#importamos las claves de la api
from config.keys import api_service_name, api_version, DEVELOPER_KEY, allowed_fields
from concurrent.futures import ThreadPoolExecutor
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



def getComment(link, maxResults=100):
    comments = []
    video_response = youtube.videos().list(
        part='snippet',
        id=link
    ).execute()
    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']
    nextPageToken = None

    def process_comment(item):
        comment = item['snippet']['topLevelComment']['snippet']
        if comment['authorChannelId']['value'] != uploader_channel_id:
            #seleccionamos solo los campos permitidos ['authorDisplayName', 'publishedAt', 'likeCount', 'textOriginal']
            return {key: comment[key] for key in allowed_fields}
        return None

    with ThreadPoolExecutor() as executor:
        while len(comments) < maxResults:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=link,
                maxResults=100,
                pageToken=nextPageToken
            )
            response = request.execute()
            comment_results = executor.map(process_comment, response['items'])
            comments.extend([comment for comment in comment_results if comment is not None])
            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break
    return pd.DataFrame(comments)


