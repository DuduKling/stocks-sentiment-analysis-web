import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

nltk.download('movie_reviews')
nltk.download('punkt')

textBlobber = Blobber(analyzer=NaiveBayesAnalyzer())

from afinn import Afinn

afinn = Afinn()


def processData(formData, dataSource):
    try:
        if 'checkboxSentimentAnalysisNLTK' in formData:
            calculateSentiment(
                dataSource,
                'nltkCompound',
                lambda text: sia.polarity_scores(text)['compound'],
                getDefaultTextAnalysis
            )
    except:
        return ['Could not analyse the sentiment with NLTK']

    try:
        if 'checkboxSentimentAnalysisTextblobPatternAnalyzer' in formData:
            calculateSentiment(
                dataSource,
                'textblob',
                lambda text: TextBlob(text).sentiment.polarity,
                getDefaultTextAnalysis
            )
    except:
        return ['Could not analyse the sentiment with Textblob']

    try:
        if 'checkboxSentimentAnalysisTextblobNaiveBayesAnalyzer' in formData:
            calculateSentiment(
                dataSource,
                'textblobNaiveBayes',
                lambda text: textBlobber(str(text)).sentiment.classification,
                getTextblobNaiveBayesTextAnalysis
            )
    except:
        return ['Could not analyse the sentiment with Textblob NaiveBayes']

    try:
        if 'checkboxSentimentAnalysisAFINN' in formData:
            calculateSentiment(
                dataSource,
                'afinn',
                lambda text: afinn.score(text),
                getDefaultTextAnalysis
            )
    except:
        return ['Could not analyse the sentiment with AFFIN']

    return dataSource

def calculateSentiment(df, name, calculateFunc, resultFunc):
    listTexts = df['CleanText']
    listTexts = listTexts.apply(lambda x: str(x)[:512]) # Transformers limit

    df[name] = listTexts.apply(lambda text: calculateFunc(text));
    df[f'{name}Score'] = df[name].apply(lambda score: resultFunc(score))

def getDefaultTextAnalysis(value):
    if isinstance(value, float):
        if value < 0:
            return 'Negative'
        elif value == 0:
            return 'Neutral'
        else:
            return 'Positive'

def getTextblobNaiveBayesTextAnalysis(value):
    if value == 'neg':
        return 'Negative'
    elif value == 'pos':
        return 'Positive'
    else:
        return 'Neutral'
