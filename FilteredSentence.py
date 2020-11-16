
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation


# as sentenças vindas do sentence filtering estarão contidas
# em Movie.filtered_sentences

# instanciar essas sentenças aqui nessa classe


class FilteredSentence:

    def __init__(self, id, sentence):
        
        self._id = id
        self._in_summary = False
        self._raw_sentence = sentence
        self._preprocessed_sentence = ""
        
        self.preprocessing_phase()


    '''
       preprocessing_phase(self):

       for each sentence object, the punctuation is removed,
       and also the stopwords. 

    '''

    def preprocessing_phase(self):
     
        
        sentece = strip_punctuation(self._raw_sentence)
        sentece = remove_stopwords(self._raw_sentence)
        self._preprocessed_sentence = sentece.lower()


    @property
    def preprocessed_sentence(self):
        return._preprocessed_sentece

    @property
    def is_in_summary(self):
        return._in_summary


    def __str__(self):

        return ' '.join(self._raw_sentence)