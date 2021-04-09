import os
import re
import unicodedata
from bs4 import BeautifulSoup
import nltk
import spacy
from contractions import contractions_dict
from nltk.tokenize.toktok import ToktokTokenizer

try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en")
    nlp = spacy.load("en_core_web_sm")

tokenizer = ToktokTokenizer()

nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('english')

def preProcessData(formData, dataSource):
    try:
        dataSource['CleanText'] = clean(dataSource['Text'], formData)
        dataSource = dropRows(dataSource, formData)
    except:
        return ['Could not pre process the retrieved data']

    return dataSource

def clean(textlist, formData):
    cleanedTextList = []
    for doc in textlist:
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc) # remove linhas em branco
        doc = re.sub(' +', ' ', doc) # remove linhas em branco

        if 'checkboxTextProcessingRemoveTwitterSpecialChar' in formData:
            doc = remove_special_twitter(doc) # remove especiais do twitter

        if 'checkboxTextProcessingRemoveHtmlTags' in formData:
            doc = strip_html_tags(doc) # remove links

        if 'checkboxTextProcessingRemoveSpecialChararacters' in formData:
            doc = remove_special_characters(doc) # remove caracteres especiais 

        if 'checkboxTextProcessingRemoveAccent' in formData:
            doc = remove_accent(doc) # remove acentuação

        if 'checkboxTextProcessingRemoveNumbers' in formData:
            doc = remove_numbers(doc) # remove números


        if 'checkboxTextProcessingStopwords' in formData:
            doc = remove_stopwords(doc) # remove stopwords

        if 'checkboxTextProcessingExpandContractions' in formData:
            doc = expand_contractions(doc) # expande contrações

        if 'checkboxTextProcessingStemming' in formData:
            doc = stemmer(doc) # stemming

        if 'checkboxTextProcessingLemmatization' in formData:
            doc = lemmatize(doc) # lemmatização

        doc = doc.lower() # texto em caixa baixa
        doc = doc.strip() # remove espaços em branco iniciais e finais
        doc = re.sub(r'\s+', ' ', doc) # remove espaços em branco desnecessarios

        cleanedTextList.append(doc)
    return cleanedTextList

def dropRows(df, formData):
    if 'checkboxTextProcessingDropDuplicates' in formData:
        df = df.drop_duplicates(subset = 'CleanText', keep = 'last') # Remove duplicadas

    df = df[df['CleanText'].str.strip().astype(bool)] # Remove textos em branco

    return df

'''Remove especiais do twitter'''
def remove_special_twitter(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text) # Remove mentions
    text = re.sub(r'#', '', text) # Remove hashtags
    text = re.sub(r'RT : ', '', text) # Remove retweets
    return text

'''Remove caracteres especiais'''
def remove_special_characters(text, remove_digits=False):
    special_char_pattern = re.compile(r'([{.(-)!}])')
    text = special_char_pattern.sub(" \\1 ", text)

    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text

'''Remove acentos'''
def remove_accent(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

'''Remove links'''
def strip_html_tags(text):
    text = re.sub(r"http[s]?://\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

'''Remove stopwords'''
def remove_stopwords(text):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

'''Lematização'''
def lemmatize(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

'''Remove números'''
def remove_numbers(text):
    text = re.sub(r'[0-9]', '', text)
    return text

'''Stemming'''
def stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text

'''Expande contrações'''
def expand_contractions(text, contraction_mapping=contractions_dict):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
        if contraction_mapping.get(match) \
        else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    try:
        expanded_text = contractions_pattern.sub(expand_match, text)
        expanded_text = re.sub("'", "", expanded_text)
    except:
        return text
    return expanded_text
