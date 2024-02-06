from pysentimiento import create_analyzer
import transformers

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="es")
""" se devuelve varios objetos de tipo AnalyzerOutput, cada uno con un texto y sus respectivas probabilidades de ser positivo, negativo o neutral
,se busca solo devolver output
AnalyzerOutput(output=POS, probas={POS: 0.961, NEU: 0.033, NEG: 0.006}) """


def get_sentiment(dataframe):
    sentimientos = analyzer.predict(dataframe['textPreprocess'])
    dataframe['sentiment'] = [sentimiento.output for sentimiento in sentimientos]
    distribution = distribution_sentiment(dataframe)
    return dataframe, distribution

def distribution_sentiment(dataframe):
    sentiment = dataframe['sentiment'].value_counts(normalize=True)
    return sentiment.to_dict()