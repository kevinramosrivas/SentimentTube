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


def preprocess_comments(dataframe):
    ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=4, disable_pr_bar=False)
    #medir el tiempo de ejecucion
    timeinit = time.time()
    dataframe['textPreprocess'] =  dataframe['textOriginal'].p_apply(preprocess_tweet)
    timeend = time.time()
    print('Tiempo de ejecucion preprocesamiento: ', timeend - timeinit)
    return dataframe





def preprocess_transcript(dataframe):
    ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=10, disable_pr_bar=False)
    dataframe['textPreprocess'] = dataframe['text'].p_apply(preprocess_tweet)
    return dataframe


