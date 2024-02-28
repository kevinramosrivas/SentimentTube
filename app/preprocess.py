from pysentimiento.preprocessing import preprocess_tweet
import multiprocessing as mp
import time
from parallel_pandas import ParallelPandas
#importar la libreria reg
import re
import nltk
# nltk.download('stopwords') #usar solo una vez
from nltk.corpus import stopwords

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
def calculate_split_factor(n_rows, n_cpu):
    print("Numero de filas a procesar: ",n_rows)
    print("Numero de cpus usadas: ",n_cpu)
    print("Numero de particiones: ",n_rows // n_cpu + 1)
    return n_rows // n_cpu + 1


def preprocess_comments(dataframe):
    split_factor = calculate_split_factor(len(dataframe), mp.cpu_count())
    ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=split_factor, disable_pr_bar=False)
    #medir el tiempo de ejecucion
    timeinit = time.time()
    dataframe['textPreprocess'] =  dataframe['textOriginal'].p_apply(preprocess_text)
    timeend = time.time()
    print('Tiempo de ejecucion preprocesamiento: ', timeend - timeinit)
    return dataframe




def preprocess_transcript(dataframe):
    split_factor = calculate_split_factor(len(dataframe), mp.cpu_count())
    #guardar el dataframe en un archivo csv
    if(type(dataframe) == str):
        return dataframe
    ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=split_factor, disable_pr_bar=False)
    dataframe['textPreprocess'] = dataframe['text'].p_apply(preprocess_text)
    return dataframe


def preprocess_text(text):
    text = preprocess_tweet(text)
    stop_words = set(stopwords.words('spanish'))
    # usar la libreria reg para eliminar los caracteres especiales
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-ZñÑáéíóúÁÉÍÓÚ]', ' ', text)
    text = text.lower()
    tokens = text.split()
    tokens = list(filter(lambda token: token not in stop_words, tokens))
    text = ' '.join(tokens)
    return text


