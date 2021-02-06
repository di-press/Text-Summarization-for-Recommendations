import numpy as np
import math
import FilteredSentence 


def centroid_construction(selected_tf_idf_dimensios):
    '''
    This function computes the centroid
    by summing each babelsynset 300 dimensions.

    Parameters:

        selected_tf_idf_dimensions(list): list containing
        each vector representation of each term selected by tf_idf

    Returns:

        centroid_embbedings (np.ndarray): the computed centroid
    '''

    centroid_embbeding = np.zeros(300, float)    

    for current_embbeding in selected_tf_idf_dimensios:

        # summing each dimension of the tweo vectors:
        centroid_embbeding += current_embbeding

    return centroid_embbeding


def filtered_sentence_embbeding(babelsynsets_dimensions):

    '''
    This function computes the embbeding of a 
    FilteredSentence object.

    Parameters:

        babelsynsets_dimensions(list): list containing
        each vector representation of the babelsynsets
        in a sentence

    Returns:

        temp_embbeding (np.ndarray): the correspondent
        embbeding of a sentence
    '''
    temp_embbeding = np.zeros(300, float)    

    for current_embbeding in babelsynsets_dimensions:
       
        current_embbeding = np.array(current_embbeding)
        
        temp_embbeding += current_embbeding

    # generating files only for testing:
    with open("filtered_sentence_embbeding.txt", 'w', encoding='utf-8') as f:
        print(temp_embbeding, file=f)
    
    return temp_embbeding



def cosine_similarity(centroid_embbeding, sentence_embbeding):

    '''
    This function computes the cosine similarity
    between two vectors.

    Parameters:

        sentence_embbeding (np.ndarray): the correspondent
        embbeding of a sentence
        centroid_embbeding(np.ndarray): the centroid embbeding
        for a movie

    Returns:

        cosine_similarity (float): the cosine similarity between
            the two vectors
        
    '''
    # computes the Frobenius norm:
    centroid_norm = np.linalg.norm(centroid_embbeding, ord= 2)
    sentence_embbeding_norm = np.linalg.norm(sentence_embbeding, ord= 2)
    
    if centroid_norm == 0 or sentence_embbeding_norm == 0:
        print("Log: at least one zero vector was encountered")
        return np.nan

    dot_product_embbedings = np.dot(centroid_embbeding, sentence_embbeding)
    cosine_denominator = centroid_norm * sentence_embbeding_norm
    cosine_similarity = dot_product_embbedings / cosine_denominator

    return cosine_similarity
    