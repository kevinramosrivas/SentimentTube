from pysentimiento import create_analyzer
import transformers

transformers.logging.set_verbosity(transformers.logging.ERROR)

emotion_analyzer = create_analyzer(task="emotion", lang="es")


def get_emotion(dataframe):
    emotions = emotion_analyzer.predict(dataframe['textPreprocess'])
    dataframe['emotion'] = [emotion.output for emotion in emotions]
    distribution_emotions = calculate_distribution(dataframe)
    return dataframe, distribution_emotions


def get_emotion_full_text(dataframe):
    #unir todos los textos en un solo string
    full_text = ' '.join(dataframe['textPreprocess'])
    emotions = emotion_analyzer.predict(full_text)
    return emotions


def calculate_distribution(dataframe):
    emotions = dataframe['emotion'].value_counts(normalize=True)
    #retornar los valores como un diccionario
    return emotions.to_dict()