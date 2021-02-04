
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
import numpy as np




class FilteredSentence:

    def __init__(self, id, sentence):
        
        self._id = id
        #self._in_summary = False
        self._raw_sentence = sentence
        self._number_of_words = len(self._raw_sentence.split())  
        self._preprocessed_sentence = ""
        self._preprocessed_words = []
        self._score = 0
        self._sentence_embbeding = np.zeros(300, float)
        self._babelsynsets_words = []
        
        #self.preprocessing_phase()


    '''
       preprocessing_phase(self):

       for each sentence object, the punctuation is removed,
       and also the stopwords. 

    '''

    def preprocessing_phase(self):

        #self._number_of_words = len(self._raw_sentence.split())  
        sentence = strip_punctuation(self._raw_sentence)
        sentence = remove_stopwords(sentence)
        # sentence = sentence.lower()
        self._preprocessed_sentence = sentence
        self._preprocessed_words = sentence.split()


    @property
    def preprocessed_sentence(self):
        return self._preprocessed_sentence

    @property
    def raw_sentence(self):
        return self._raw_sentence

    #@property
    #def is_in_summary(self):
    #    return self._in_summary

    @property
    def score(self):
        return self._score

    
    def add_score(self, score_value):
        self._score = score_value

    @property
    def sentence_embbeding(self):
        return self._sentence_embbeding

    
    def add_sentence_embbeding(self, embbeding):
        self._sentence_embbeding = embbeding


    @property
    def preprocessed_words(self):
        return self._preprocessed_words

    @property
    def babelsynsets_words(self):
        return self._babelsynsets_words

    #@babelsynsets_words.setter
    #def babelsynsets_words(self, word_and_babelsynset):
        #self._babelsynsets_words.append(word_and_babelsynset)

    @property 
    def number_of_words(self):
        return self._number_of_words
    
    def add_babelsynsets_words(self, word_and_babelsynset):
        self._babelsynsets_words.append(word_and_babelsynset)


    def __str__(self):

        return ''.join(self._raw_sentence)


if __name__ == "__main__":

    phrase = "I was never late, untill the day I realized I had dreams."

    new_filtered_sentence = FilteredSentence(1, phrase)
    final = new_filtered_sentence.preprocessed_sentence
    print(final)
    print(new_filtered_sentence.__str__())
