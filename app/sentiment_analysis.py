from pysentimiento import create_analyzer
import transformers
from flask import jsonify
import time
from parallel_pandas import ParallelPandas
import multiprocessing as mp
import multiprocessing
from collections import Counter

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="es")
""" se devuelve varios objetos de tipo AnalyzerOutput, cada uno con un texto y sus respectivas probabilidades de ser positivo, negativo o neutral
,se busca solo devolver output
AnalyzerOutput(output=POS, probas={POS: 0.961, NEU: 0.033, NEG: 0.006}) """
ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=8, disable_pr_bar=False)

def process_emotion(emotion):
    return emotion.output

def get_sentiment(dataframe):
    #medir el tiempo de ejecucion
    timeinit = time.time()
    sentimientos = analyzer.predict(dataframe['textPreprocess'])
    with multiprocessing.Pool(mp.cpu_count()) as pool:
        dataframe['sentiment'] = pool.map(process_emotion, sentimientos)
    dict_comments = dataframe.to_dict(orient='records')
    distribution = get_distribution(dataframe)
    word_count = word_counts(dataframe)
    #medir el tiempo de ejecucion
    timeend = time.time()
    print('Tiempo de ejecucion analisis de sentimiento: ', timeend - timeinit)
    return dict_comments, distribution, word_count



def get_distribution(dataframe):
    #seleccionar la distribucion de sentimientos
    distribution = dataframe['sentiment'].value_counts().to_dict()
    return distribution

def word_counts(dataframe):
    texto = " ".join(dataframe["textPreprocess"])
    word_counts = Counter(texto.split())
    most_common_words = dict(word_counts.most_common(10))
    return most_common_words