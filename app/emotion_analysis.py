from pysentimiento import create_analyzer
import transformers
from collections import Counter
import concurrent.futures

transformers.logging.set_verbosity(transformers.logging.ERROR)

emotion_analyzer = create_analyzer(task="emotion", lang="es")




def get_emotion(dataframe):
    emotions = emotion_analyzer.predict(dataframe['textPreprocess'])

    def process_emotion(emotion):
        return emotion.output

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_emotion, emotions)
        dataframe['emotion'] = list(results)

    distribution_emotions = calculate_distribution(dataframe)
    return dataframe, distribution_emotions


def get_emotion_full_text(dataframe):
    #unir todos los textos en un solo string
    full_text = ' '.join(dataframe['textPreprocess'])
    emotions = emotion_analyzer.predict(full_text)
    return emotions


def calculate_distribution(dataframe):
    emotions = Counter(dataframe['emotion'])
    return emotions
