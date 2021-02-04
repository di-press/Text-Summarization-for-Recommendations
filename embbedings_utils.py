import numpy as np
import math
import FilteredSentence 


def centroid_construction(selected_tf_idf_dimensios):

    centroid_embbeding = np.zeros(300, float)    

    for current_embbeding in selected_tf_idf_dimensios:

        
        centroid_embbeding += current_embbeding

    return centroid_embbeding


def filtered_sentence_embbeding(babelsynsets_dimensions):

    
    temp_embbeding = np.zeros(300, float)    

    for current_embbeding in babelsynsets_dimensions:
       
        current_embbeding = np.array(current_embbeding)
        
        temp_embbeding += current_embbeding

    with open("filtered_sentence_embbeding.txt", 'w', encoding='utf-8') as f:
        print(temp_embbeding, file=f)
    
    return temp_embbeding



def cosine_similarity(centroid_embbeding, sentence_embbeding):

    centroid_norm = np.linalg.norm(centroid_embbeding, ord= 2)
    sentence_embbeding_norm = np.linalg.norm(sentence_embbeding, ord= 2)
    
    if centroid_norm == 0 or sentence_embbeding_norm == 0:
        print("Log: at least one zero vector was encountered")
        return np.nan

    dot_product_embbedings = np.dot(centroid_embbeding, sentence_embbeding)
    cosine_denominator = centroid_norm * sentence_embbeding_norm
    cosine_similarity = dot_product_embbedings / cosine_denominator

    return cosine_similarity
    