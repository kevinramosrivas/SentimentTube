from pysentimiento import create_analyzer
import transformers

transformers.logging.set_verbosity(transformers.logging.ERROR)

analyzer = create_analyzer(task="sentiment", lang="es")



def get_sentiment(dataframe):
    dataframe['sentiment'] = dataframe['textPreprocess'].apply(analyzer.predict)
    return dataframe
