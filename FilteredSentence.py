
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
import numpy as np


# as sentenças vindas do sentence filtering estarão contidas
# em Movie.filtered_sentences

# instanciar essas sentenças aqui nessa classe


class FilteredSentence:

    def __init__(self, id, sentence):
        
        self._id = id
        self._in_summary = False
        self._raw_sentence = sentence
        self._preprocessed_sentence = ""
        self._preprocessed_words = []
        self._filtered_sentence_score = 0
        self._sentence_embbeding = np.zeros(300, float)
        self._babelsynsets_words = []
        
        self.preprocessing_phase()


    '''
       preprocessing_phase(self):

       for each sentence object, the punctuation is removed,
       and also the stopwords. 

    '''

    def preprocessing_phase(self):
            
        sentence = strip_punctuation(self._raw_sentence)
        sentence = remove_stopwords(sentence)
        # sentence = sentence.lower()
        self._preprocessed_sentence = sentence
        self._preprocessed_words = sentence.split()


    @property
    def preprocessed_sentence(self):
        return self._preprocessed_sentence

    @property
    def is_in_summary(self):
        return self._in_summary

    @property
    def filtered_sentence_score(self):
        return self._filtered_sentence_score

    @filtered_sentence_score.setter
    def filtered_sentence_score(self, score_value):
        self._filtered_sentence_score = score_value

    @property
    def sentence_embbeding(self):
        return self._sentence_embbeding

    @sentence_embbeding.setter
    def sentence_embbeding(self, embbeding):
        self._sentence_embbeding = embbeding


    @property
    def preprocessed_words(self):
        return self._preprocessed_words

    @property
    def babelsynsets_words(self):
        return self._babelsynsets_words
    
    #fazer query das words

    def __str__(self):

        return ''.join(self._raw_sentence)


if __name__ == "__main__":

    phrase = "I was never late, untill the day I realized I had dreams."

    new_filtered_sentence = FilteredSentence(1, phrase)
    final = new_filtered_sentence.preprocessed_sentence
    print(final)
    print(new_filtered_sentence.__str__())
