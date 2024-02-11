from pysentimiento.preprocessing import preprocess_tweet
import multiprocessing as mp
import time
from parallel_pandas import ParallelPandas

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
ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=8, disable_pr_bar=False)

def preprocess_comments(dataframe):
    #medir el tiempo de ejecucion
    timeinit = time.time()
    dataframe['textPreprocess'] =  dataframe['textOriginal'].p_apply(preprocess_tweet)
    timeend = time.time()
    print('Tiempo de ejecucion preprocesamiento: ', timeend - timeinit)
    return dataframe





def preprocess_transcript(dataframe):
    dataframe['textPreprocess'] = dataframe['text'].p_apply(preprocess_tweet)
    return dataframe


