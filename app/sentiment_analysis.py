from pysentimiento import create_analyzer
import transformers
from flask import jsonify
import time
from parallel_pandas import ParallelPandas
import multiprocessing as mp



transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="es")
""" se devuelve varios objetos de tipo AnalyzerOutput, cada uno con un texto y sus respectivas probabilidades de ser positivo, negativo o neutral
,se busca solo devolver output
AnalyzerOutput(output=POS, probas={POS: 0.961, NEU: 0.033, NEG: 0.006}) """
ParallelPandas.initialize(n_cpu=mp.cpu_count(), split_factor=40, disable_pr_bar=False)

def get_sentiment(dataframe):
    #medir el tiempo de ejecucion
    timeinit = time.time()
    sentimientos = analyzer.predict(dataframe['textPreprocess'])
    dataframe['sentiment'] = list(sentimientos)
    dataframe = select_only_sentiment(dataframe)
    dict_comments = dataframe.to_dict(orient='records')
    distribution = get_distribution(dataframe)
    #medir el tiempo de ejecucion
    timeend = time.time()
    print('Tiempo de ejecucion analisis de sentimiento: ', timeend - timeinit)
    return dict_comments, distribution

def select_only_sentiment(dataframe):
    #se;eccopmar solo el output de cada sentimiento
    dataframe['sentiment'] = dataframe['sentiment'].p_apply(lambda x: x.output)
    return dataframe

def get_distribution(dataframe):
    #seleccionar la distribucion de sentimientos
    distribution = dataframe['sentiment'].value_counts().to_dict()
    return distribution