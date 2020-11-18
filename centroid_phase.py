# fazer a função que faz a query do babelnet

import numpy as np
import math
import FilteredSentence 


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

'''
    sentences_embbedings is a list of sentences objects.
    For each sentence object, the score for its embbeding
    is calculated as in formula (4) of the paper.

    Only the sentence embbedings having a non NaN value
    are going to be inlcuded in the filtered_sentences_score dictionary.

    This function returns a dictionary with sentence objects,
    and for each object, its embbeding and score were attributed
    in this function.
'''

def sentence_scoring(centroid_embbeding, sentences_embbedings):

    filtered_sentences_scores = {}

    for sentence_object in sentences_embbedings:

        current_sentence_embbeding = sentence_object.sentence_embbeding
        current_sentence_score = cosine_similarity(centroid_embbeding, current_sentence_embbeding)

        if current_sentence_score != np.nan:

            filtered_sentences_scores[sentence_object] = current_sentence_score
            sentence_object.filtered_sentence_score = current_sentence_score

    
    return filtered_sentences_scores

"""

    filtered_sentences_score is a dict contianing a sentence_object
    mapped with its score value.

    Count by word is a boolean value. When count_by_word is passed as True,
    the summary is formed untill the maximum number of words is reached.

    When count_by_word is passed as False, the summary is formed until the
    desired number of sentences is reached.

    discard_threshold is the value of cosine similarity between a sentence already
    included in the summary and a sentence to be included.

    max_number_elements is the number of words/sentences that are desired
    to be in the summary.
"""

def sentence_selection(filtered_sentences_scores, discard_threshold, max_number_of_elements, count_by_word):

    # order the dictionary by score of each sentence embbeding in descending order.
    # sorted_filtered_sentences score is a list, in whic each element contain
    # the sentence object and its score value  
    sorted_filtered_sentences_score = sorted(filtered_sentences_scores.items(), key=lambda x : x[1], reverse=True)          

    candidates_sentences_summary = []

    for pair in sorted_filtered_sentences_score:
        #candidates_sentences_summary is going to contain only sentence_objects
        candidates_sentences_summary.append(pair[0])

    sentences_in_summary = []

    # the first sentence object in the candidates_sentence_summary
    # is the sentence that had the highest score in the sorted_filtered_sentences_score;
    # so, this sentence object is surely included in the summary list (sentences_in_summary):

    highest_score_sentence = candidates_sentences_summary.pop(0)
    sentences_in_summary.append(highest_score_sentence)

    # now, the candidates_sentences_in_summary has one less element,
    # since the first sentence object element was popped.

    number_chosen_elements = 1

    #evaluating the similarity between each sentence object to be included in the summary:

    for sentence in candidates_sentences_summary:

        for included_summary_sentence in sentences_in_summary:

            current_score = cosine_similarity(included_summary_sentence, sentence)

            if current_score >= discard_threshold or current_score == np.nan:
                
                break
                        
            
            if count_by_word == True:

                number_chosen_elements = number_chosen_elements + sentence.number_of_words

                if number_chosen_elements <= max_number_of_elements:
                
                    sentences_in_summary.append(sentence)
                else:
                    return sentences_in_summary
            
            # if count_by_word is false, means that the number of sentences is counted:
            if count_by_word == False:

                sentences_in_summary.append(sentence)
                number_chosen_elements = number_chosen_elements + 1

                if number_chosen_elements == max_number_of_elements:
                    
                    return sentences_in_summary

    return sentences_in_summary


def print_summary(sentences_in_summary):

    for sentence_object in sentences_in_summary:
        
        sentence_object.__str__()



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





