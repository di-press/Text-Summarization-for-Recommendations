import FilteredSentence
import numpy as np
import pandas as pd

'''
Extract the filtered sentences from the file passed as argument to this function
and instantiates each sentence in a FilteredSentence class object.

'''
def receive_filtered_sentences(filepath):

    raw_sentences_container = []

    with open(filepath) as filtered_sentences_file:
        
        current_raw_sentence = filtered_sentences_file.readline()
        id = 0
        new_filtered_sentence = FilteredSentence.FilteredSentence(id, current_sentence)
        filtered_sentences_container.append(new_filtered_sentence)
        id = id+1

        #while there are lines to be read:
        while current_raw_sentence:
            current_raw_sentence = filtered_sentences_file.readline()
            new_filtered_sentence = FilteredSentence.FilteredSentence(id, current_sentence)
            filtered_sentences_container.append(new_filtered_sentence)
            id = id+1
        
    return filtered_sentences_container

    '''
        for each FilteredSentence object in filtere_sentences_container, the vocabulary
        is formed by its preprocessed sentence (after removing punctuation and stopwords). 
    '''

    def tf(frequency_table):
            
        
    def tf_idf(filtered_sentences_container):

        vocabulary = []

        for filtered_sentence_object in filtered_sentences_container:
            vocabulary.append(filtered_sentence_object.preprocessed_sentence())
        
        corpus = np.array(vocabulary)
        count = CountVectorizer()
        bag_of_words = count.fit_transform(corpus) 
        feature_names = count.get_feature_names()

        frequency_table = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)
        frequency_table = frequency_table.transpose()

        # frequency table is word x document, where the number is the frequency in the document:
        #             documents
        #            0  1  2  3
        # am         0  2  1  0
        # be         2  2  2  2
        # da         0  0  0  3
        # do         2  0  2  3



            
           


