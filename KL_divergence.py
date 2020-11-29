#arrumar o "apos erro"
import counter_occurrences as count_occur
import numpy as np

def KL_divergence(frequency_corpora_reviews, frequency_corpora_BNC):

    """Computes the discrete KL divergence for a noun present in the corpora review.
        KL value = (frequency_corpora_reviews) * log(frequency_corpora_reviews/frequency_corpora_BNC)

    Args:
        frequency_corpora_reviews (int): The number of occurrences of the noun in the reviews
        corpora; it's the term "ca" in the formula described in the paper

        frequency_corpora_BNC (int): The number of occurrences of the noun in the BNC
        corpora; it's the term "cb" in the formula described in the paper

    Returns:
        KL (double): The KL value calculated for the noun
        
    """
    
    #by definition, if the number of occurrences of the noun in the BNC
    #corpora is zero, that means that the kl value for this noun in infinity:
    if frequency_corpora_BNC == 0:
        return np.inf

    division_term = (frequency_corpora_reviews/frequency_corpora_BNC)
    second_term= np.log(division_term)
    KL= frequency_corpora_reviews*second_term

    return (KL)

def KL_nouns_values(corpora_BNC, corpora_reviews):

    """Computes the KL value for each noun present in the corpora of reviews,
    using the previous generated files: "corpora_reviews.txt" and 
    "corpora_BNC.txt"

    Args:
        
    Returns:
        KL_values (dict): Contains the KL value associated to each noun of the corpora review,
        for all nouns presents in the corpora review
    """
    #counts the occurrence of each noun in the following corporas:
    count_nouns_reviews = count_occur.counting_occurrences_list(corpora_reviews)
    count_nouns_BNC = count_occur.counting_occurrences_list(corpora_BNC)
    
    
    KL_values = {}

    for noun in count_nouns_reviews:
        #frequency_corpora_reviews is never zero;
        #frequency_corpora_reviews is the number of occurrences of 
        #the current noun in the reviews corpora:
        frequency_corpora_reviews = count_nouns_reviews[noun] 

        #frequency_corpora_BNC is the number of occurrences of
        #the current now in the BNC corpora:
        frequency_corpora_BNC = count_nouns_BNC[noun]
        
        #KL_values is a dict containing the noun and it's kl_value, for all nouns
        #in the corpora review:
        KL_values[noun] = KL_divergence(frequency_corpora_reviews, frequency_corpora_BNC)

    
    return KL_values


def epsilon_aspects_extraction(KL_values, threshold, destiny_file):

    """Given a certain threshold for KL divergence, this function extracts 
        aspects from the KL_values dict

    Args:
        KL_values (dict): dict containing each noun in the corpora review
        associated with it's KL value

        threshold (double): The Epsilon cited in the paper

        destiny_file(str): the file that is going to contain all the
        aspects extracted. If printing is not desired, this parameter
        should be passed as "none"

    Returns:
        aspects(dict): A dict that relates each aspect to it's KL value
    """
    aspects={}

    for noun in KL_values:
        if KL_values[noun] > threshold:
            aspects[noun] = KL_values[noun]
    
    if destiny_file != "none":
        
        with open(destiny_file, 'a+', encoding="utf-8") as f:
            print(aspects, file=f)

    return aspects

