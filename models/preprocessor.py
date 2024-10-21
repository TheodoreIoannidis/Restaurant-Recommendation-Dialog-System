import string
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab', quiet=True)
stopwords = nltk.corpus.stopwords.words("english")


class Preprocessor:
    """
    Preprocess user input before intent prediction
    """
    def __init__(self):
        self.stemmer = nltk.stem.PorterStemmer()
        self.stopwords = nltk.corpus.stopwords.words("english")

    @staticmethod
    def _remove_punctuation_and_stopwords(tokens):
        filtered_tokens = [token for token in tokens if token not in string.punctuation]
        return filtered_tokens

    @staticmethod
    def _get_stemmed_tokens(tokens):
        stemmer = nltk.stem.PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return stemmed_tokens

    def preprocess_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tokens = [token.lower() for token in tokens]
        tokens = self._remove_punctuation_and_stopwords(tokens)
        tokens = self._get_stemmed_tokens(tokens)
        return tokens

    def stem_word(self, word):
        return self.stemmer.stem(word)
