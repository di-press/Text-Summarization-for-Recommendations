
# antigo nome do arquivo: FilteredSentence.py
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation


# https://towardsdatascience.com/introduction-to-nlp-part-3-tf-idf-explained-cedb1fc1f7dc


# a pseudoreview is formed by the sentences filtered in the sentence filtering phase

# in the sentence filtering phase, the most important sentences in a review are
# selected, and grouped together to form a pseudo review

# each pseudo review is considered as a document in the tf-idf appliance

# colocar as pseudo-reviews vindas do sentence filtering num arquivo txt, 
# sendo que cada arquivo txt representa um filme
# fazer a função que lê o arquivo txt

# instanciar essas pseudoreviews aqui nessa classe, ler do documento texto e gerar
# os objetos pseudoreviews

# cada pseudo-review de um filme foi considerada como um documento para o tf-idf 

# futuramente: checagem estática mypi

class PseudoSentence:

    def __init__(self, id, sentence):
        
        self._id = id
        self._in_summary = False
        self._raw_sentence = sentence
        #self._preprocessed_words = []
        self._tfidf_filtered_words = {}
        self._preprocessed_sentence=[]
        
        self.preprocessing_phase()


    '''
       preprocessing_phase(self):

       for each sentence object, the punctuation is removed,
       and also the stopwords. 
       The tf-idf value for each word isn't already computed yet,
       so its value is 0.

    '''

    def preprocessing_phase(self):
     
        # self._sentence.lower()
        sentece = strip_punctuation(self._raw_sentence)
        sentece = remove_stopwords(self._raw_sentence)
        self._preprocessed_sentence = sentece.split()

        for word in self._preprocessed_sentece:

            self._tfidf_filtered_words[word] = 0

    @property
    def preprocessed_sentence(self):
        return._preprocessed_sentece


    def __str__(self):

        return ' '.join(self._raw_sentence)