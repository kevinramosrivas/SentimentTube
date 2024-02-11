from pysentimiento import create_analyzer
import transformers
from flask import jsonify
import concurrent.futures

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="es")
""" se devuelve varios objetos de tipo AnalyzerOutput, cada uno con un texto y sus respectivas probabilidades de ser positivo, negativo o neutral
,se busca solo devolver output
AnalyzerOutput(output=POS, probas={POS: 0.961, NEU: 0.033, NEG: 0.006}) """


def get_sentiment(dataframe):
    sentimientos = analyzer.predict(dataframe['textPreprocess'])

    def process_sentimiento(sentimiento):
        return sentimiento.output

    with concurrent.futures.ThreadPoolExecutor() as executor:
        sentiment_outputs = executor.map(process_sentimiento, sentimientos)

    dataframe['sentiment'] = list(sentiment_outputs)
    distribution = distribution_sentiment(dataframe)
    dict_comments = dataframe.to_dict(orient='records')
    return dict_comments, distribution

def distribution_sentiment(dataframe):
    sentiment = dataframe['sentiment'].value_counts()
    return sentiment.to_dict()