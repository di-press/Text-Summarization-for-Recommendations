# fazer a função que faz a query do babelnet

import numpy as np
import math


"""
    "babelsynsets_4471657.txt" is a file in which each line is a babelsynset
    followed by its 300 dimensions vector values, separated by space.
    This function searchs the babelsynset in the "babelsynsets_4471657.txt"
    file and retrieve its 300 dimensions values.

    If the babelsynset is founded, this function returns its 300 dimensions
    values in form of numpy array. 
    If it is not found, this function returns False
"""

def retrieve_babelsynset_dimensions(desired_babelsynset):

    with open("babelsynsets_4471657.txt", "r", encoding="utf-8") as synsets_file:

        for line in synsets_file:
            # each babelsynset has 12 characters:
            current_synset = str(line[0:12])

            if current_synset == desired_babelsynset:
                # the first element of the list is going to be the
                # desired babelsynset; so, the first element is excluded 
                # from the list, since only the 300 values are needed
                # in the centroid phase:

                desired_babelsynset_dimensions = line.partition(" ")[2]
                
                # split each dimension value in the line by space:
                desired_babelsynset_dimensions = desired_babelsynset_dimensions.split(" ")

                # the values are read as strings. The valuer are converted to float
                # values, and the "\n" character is removed:
                desired_babelsynset_dimensions = list(map(float, desired_babelsynset_dimensions))

                # converting the dimensions into numpy array:
                babelsynsets_dimensions_array = np.array(desired_babelsynset_dimensions)
                
                return babelsynsets_dimensions_array

    return False

'''
    selected_centroid_synsets is a list containing the babelsynset ID
    of the words that were previously selected through the tf-idf algorithm
    to be part of the centroid embbeding.

    This function sum the vectors of the babelsynset nasri embbedings
    (each dimension of a vector is added to the corresponding dimension
    of the other vector, and so on, as in formula 3 of the paper)
'''

def centroid_construction(selected_centroid_synsets):

    # founded_synsets is going to accuse if no synset was found
    # in Nasari embbedings file:
    founded_synsets = False

    centroid_embbeding = np.zeros(300, float)

    for current_babelsynset in selected_centroid_synsets:
        
        current_babelsynset_dimensions = retrieve_babelsynset_dimensions(current_babelsynset)

        # if it is not a boolean variable, the babelsynset was found:
        if type(current_babelsynset_dimensions) != bool:

            # a synset was found:
            founded_synsets = True

            # sum of each dimension 
            centroid_embbeding = centroid_embbeding + current_babelsynset_dimensions

    if founded_synsets == True:
        
        return centroid_embbeding
    else:
        
        return False

'''
    babelsynsets_filtered_sentences is a list of lists of babelsynsets;
    that means each list represents a set of babelsynsets representing each word
    in the sentence.
    As example: [[all synsets representing the words of sentence 1],
                 [all synsets representing the words of sentence 2],
                 etc]
    
    For each sentence, its embbeding is computed by summing each vector embbeding
    of each word in the sentence, as described in formula(4) of the paper

    If a sentence has not even a single word in the Nasari representation,
    it is discarded

    sentences_embbedings is a list that is returned by this function, and each element
    of this list represent a sentence embbeding in numpy ndarray format


def sentence_embbeding_construction(babelsynsets_filtered_sentences):

    sentences_embbedings = []

    for synsets_words_list in babelsynsets_filtered_sentences:

        representation = False        
        current_sentence_vector = np.zeros(300, float)
        
        for word_synset in synsets_words_list:

            babelsynset_dimensions = retrieve_babelsynset_dimensions(word_synset)

            if type(babelsynset_dimensions) != bool:
                
                representation = True
                current_sentence_vector = current_sentence_vector + babelsynset_dimensions

        # if representation has been evaluated to True, that means that at least
        # one word in the sentence has a babelsynset representation
        if representation == True:
            
            sentences_embbedings.append(current_sentence_vector)

    return sentences_embbedings

'''

'''
    Given a list of FilteredSentence objects, passed as parameter,
    this function compute the sentence embbeding for each
    FilteredSentence object.

    For each sentence, its embbeding is computed by summing each vector embbeding
    of each word in the sentence, as described in formula(4) of the paper

    If a sentence has not even a single word in the Nasari representation,
    it is discarded

    sentences_embbedings is a list that is returned by this function, and each element
    of this list is a FilteredSentence object, and a candidate to be included in
    the summary.

'''

def sentence_embbeding_construction(filtered_sentences):
    
    sentences_embbedings = []

    for sentence in filtered_sentences:

        representation = False        
        current_sentence_vector = np.zeros(300, float)

        current_synsets_words = sentence.babelsynsets_words

        for word_synset in current_synsets_words:
            
            babelsynset_dimensions = retrieve_babelsynset_dimensions(word_synset)

            if type(babelsynset_dimensions) != bool:
                
                representation = True
                current_sentence_vector = current_sentence_vector + babelsynset_dimensions

        # if representation has been evaluated to True, that means that at least
        # one word in the sentence has a babelsynset representation
        if representation == True:

            sentence.sentence_embbeding = current_sentence_vector       
            sentences_embbedings.append(sentence)

    return sentences_embbedings    

'''
    Function to calculate the cosine similarity between two embbedings,
    as in formula 5 of the paper.
    If one of the embbedings is a zero vector, NaN is returned,
    and the sentence is not included in the summary phase.
'''


def cosine_similarity(centroid_embbeding, sentence_embbeding):

    centroid_norm = np.linalg.norm(centroid_embbeding, 2)
    sentence_embbeding_norm = np.linalg.norm(sentence_embbeding, 2)
    
    if centroid_norm == 0 or sentence_embbeding_norm == 0:
        print("Log: at least one zero vector was encountered")
        return np.nan

    dot_product_embbedings = np.dot(centroid_embbeding, sentence_embbeding)
    cosine_denominator = centroid_norm * sentence_embbeding_norm
    cosine_similarity = dot_product_embbedings / cosine_denominator

    return cosine_similarity



if __name__ == '__main__':

    dimensions = retrieve_babelsynset_dimensions("bn:00000055n")

    if type(dimensions) != bool:
        print(dimensions)
    else:
        print("Not found")
    

    dimensions = retrieve_babelsynset_dimensions("bn:11100055n")

    if type(dimensions) != bool:
        print(dimensions)
    else:
        print("Not found")





