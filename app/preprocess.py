from pysentimiento.preprocessing import preprocess_tweet
import json
import nltk
from nltk.corpus import stopwords
import re
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
    dataframe['textPreprocess'] = dataframe['textOriginal'].apply(preprocess_tweet)
    #aplicar el preprocesamiento de remove_stopwords a la columna textPreprocess
    dataframe['textPreprocess'] = dataframe['textPreprocess'].apply(remove_stopwords)
    return dataframe

def preprocess_transcript(dataframe):
    dataframe['textPreprocess'] = dataframe['text'].apply(preprocess_tweet)
    #aplicar el preprocesamiento de remove_stopwords a la columna textPreprocess
    dataframe['textPreprocess'] = dataframe['textPreprocess'].apply(remove_stopwords)
    return dataframe

stop_words = set(stopwords.words('spanish'))
def remove_stopwords(text):
  text = re.sub(r'[^\w\s]', '', text)
  text = re.sub(r'<.*?>', '', text)
  text = re.sub(r'http\S+', '', text)
  text = re.sub(r'[^a-zA-ZñÑáéíóúÁÉÍÓÚ]', ' ', text)
  text = text.lower()
  tokens = text.split()
  tokens = [token for token in tokens if token not in stop_words]
  text = ' '.join(tokens)
  return text

