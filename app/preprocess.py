from pysentimiento.preprocessing import preprocess_tweet
import multiprocessing as mp
""" 
se tiene un array de comentarios, se deben preprocesar solo los textos de los comentarios
[{
"authorDisplayName": "@laluland9154",
"likeCount": 0,
"publishedAt": "2023-11-05T10:25:43Z",
"textOriginal": "Eres mi cantante favorito del mundo entero"
},
{
"authorDisplayName": "@laluland9154",
"likeCount": 0,
"publishedAt": "2023-11-05T10:25:43Z",
"textOriginal": "Eres mi cantante favorito del mundo entero"
}]

"""

def preprocess_comments(dataframe):
    with mp.Pool(mp.cpu_count()) as pool:
        dataframe['textPreprocess'] = pool.map(preprocess_tweet, dataframe['textOriginal'])
    #retornar un array de comentarios preprocesados, nombre de usuario, fecha de publicacion
    return dataframe


def preprocess_transcript(dataframe):
    dataframe['textPreprocess'] = dataframe['text'].apply(preprocess_tweet)
    return dataframe


