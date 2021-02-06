import Movie
import Review
import disambiguator
import tf_idf
import string
import babelsynsets_utils
import embbedings_utils
import FilteredSentence
import numpy as np
import no_disambiguation
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation



def summarizer_pipeline(disambiguation, 
                        movie, 
                        tf_idf_threshold, 
                        babelfy_API_key, 
                        discard_threshold, 
                        number_of_sentences_in_summary):

    '''
    Function that describes all the summarization pipeline in
    the paper.

    Parameters:

        disambiguation (boolean): is True, if disambiguation is desired
        movie (Movie object): the current movie in processing
        tf_idf_threshold (float): the minimum tf_idf value for a term to be selected
        babelfy_API_key (string): your Babelfy/Babelnet API key
        discard_threshold (float): the threshold for cosine similarity,
                                   to discard sentences that are too similar
        number_of_sentences_in_summary(int): the number of desired sentneces in summary

    Returns:
        summary (string)
                                    
    '''
    
    print("started centroid construction")
    centroid = centroid_pipeline(disambiguation, movie, tf_idf_threshold, babelfy_API_key)

    # file generated only for tests:
    with open("centroid_no_disambiguation.txt", 'a+', encoding='utf-8') as f:
        print(centroid, file=f)
     
    id = 0
    sentence_candidates = []
    for filtered_sentence in movie.filtered_sentences:

        # each sentence filtered in sentence filtering phase 
        # are instantiated as a FilteredSentence object:
        current_sentence = FilteredSentence.FilteredSentence(id, filtered_sentence)
        # sentence_candidates is a list containing all the FilteredSentence objects:
        sentence_candidates.append(current_sentence)
        id += 1

        # file generated only for tests:
        with open("filtered_sentences_instantiaton.txt", 'a+', encoding='utf-8') as f:
            print(sentence_candidates, file=f)
    
    # each FilteredSentence object goes to the sentence embbeding phase:
    sentence_embbedings_pipeline(disambiguation, sentence_candidates, babelfy_API_key)

    for filtered_sentence in sentence_candidates:

        # the cosine similarity value between each FilteredSentence and the centroid 
        # is the sentence score:
        score = embbedings_utils.cosine_similarity(centroid, filtered_sentence.sentence_embbeding)
        filtered_sentence.add_score(score)
    
    # the FilteredSentences objects are sorted in descending order of score value:
    sorted_sentences_by_score = ordering_by_similarity(sentence_candidates)

    # the sentences are selected to the summary:
    sentences_in_summary = sentence_selection(sorted_sentences_by_score, discard_threshold, number_of_sentences_in_summary)

    summary = summary_string(sentences_in_summary, movie)
    
    return summary


def centroid_pipeline(disambiguation, movie, tf_idf_threshold, babelfy_API_key):

    '''
    Function that describes the construction of the centroid embbeding.

    Parameters:

        disambiguation (boolean): is True, if disambiguation is desired
        movie (Movie object): the current movie in processing
        tf_idf_threshold (float): the minimum tf_idf value for a term to be selected
        babelfy_API_key (string): your Babelfy/Babelnet API key
    
    Returns:

        centroid (np_ndarray): the computed 300 dimensions centroid embbeding
                                    
    '''

    if disambiguation:
        
        print("started disambiguation.")
        disambiguator.disambiguate_raw_reviews(movie.reviews, babelfy_API_key)
    
        babelsynsets_documents = []

        for review in movie.reviews:
            
            current_review_document = ""
            
            # each pair represents a tuple (word, babelsynset)
            for pair in review.nouns_and_babelsynsets:
                # pair[1] is the babelsynset representation of the current pair:
                current_review_document += pair[1] + " "
            
            # the babelsynsets are going to be processed by tf_idf algorithm.
            # each review, composed by babelsynsets, is considered
            # as a document to tf_idf:
            babelsynsets_documents.append(current_review_document)
            
        
        #print(babelsynsets_documents)
        print("started tf_idf selection")
        
        # the babelsynsets having a tf_idf value greater than the tf_idf_threshold
        # are selected:
        selected_tf_idf_synsets = tf_idf.tf_idf_centroid_selection(babelsynsets_documents, tf_idf_threshold) 

        print("selected synsets from tf-idf")

        # for each babelsynset selected through tf_idf algorithm, 
        # its 300 dimensions are retrieved from "synsets_db_optimized.db":
        selected_tf_idf_dimensions = babelsynsets_utils.search_in_synsets_db_optimized(selected_tf_idf_synsets) 
        
        print("going to centroid phase")
        # the centroid, representing the meaning of the reviews, is formed
        # through the computation of the babelsynsets dimensions:
        centroid = embbedings_utils.centroid_construction(selected_tf_idf_dimensions)
    
    # if disambiguation is not desired:
    else:

        # without disambiguating, words are the input of tf_idf algorithm.
        # stemming is not performed.
        documents_for_tf_idf = []

        for review in movie.reviews:

            processed_review = strip_punctuation(review.raw_review)
            processed_review = remove_stopwords(processed_review)
            # now, processed_review is a document going to tf-idf phase,
            # and each processed review is considered as a document.

            documents_for_tf_idf.append(processed_review)
        
        print("started tf_idf selection")
        
        # given a certain tf_idf_threshold, the words havin a tf_idf greater than
        # this value are selected:
        selected_tf_idf_words = tf_idf.tf_idf_centroid_selection(documents_for_tf_idf, tf_idf_threshold)
        print("selected words from tf-idf")

        # given the selected words from tf)idf algorithm,
        # its babelsynset representation is matched with the first
        # representation encountered:
        synsets_to_search = no_disambiguation.mapping_words_and_babelsysnets(selected_tf_idf_words, babelfy_API_key)
        
        # the babelsynsets dimensions of the tf_idf selected
        # words are retrieved:
        selected_tf_idf_dimensions = babelsynsets_utils.search_in_synsets_db_optimized(synsets_to_search) 
        
        print("going to centroid phase")

        # the babelsynsets dimensions go to centroid phase:
        centroid = embbedings_utils.centroid_construction(selected_tf_idf_dimensions)

    return centroid




def sentence_embbedings_pipeline(disambiguation, sentence_candidates, babelfy_API_key):

    '''
    Function that computes the sentences embbedings for each filtered sentence.

    Parameters:

        disambiguation (boolean): is True, if disambiguation is desired
        babelfy_API_key (string): your Babelfy/Babelnet API key
        sentence_candidates (list): contains FilteredSentences objects
    
    Returns:

        None
                                    
    '''
    
    if disambiguation:
        
        print("started filtered sentences embbedings construction with disambiguation.")
        disambiguator.disambiguate_filtered_sentence(sentence_candidates, babelfy_API_key)

    else:
        print("started filtered sentences embbedings construction.")
        no_disambiguation.process_filtered_sentences(sentence_candidates, babelfy_API_key)
    
    for filtered_sentence in sentence_candidates:
        
        filtered_sentence_babelsynset = []

        for pair in filtered_sentence.babelsynsets_words:
            # pair is a tuple: (word, babelsynset representation)
            filtered_sentence_babelsynset.append(pair[1])
        
        # the babelsynsets dimensions of a FilteredSentence are retrieved:
        babelsynsets_dimensions = babelsynsets_utils.search_in_synsets_db_optimized(filtered_sentence_babelsynset)

        # the embbeding of the current FilteredSentence object is computed:
        current_sentence_embbeding = embbedings_utils.filtered_sentence_embbeding(babelsynsets_dimensions)
        
        filtered_sentence.add_sentence_embbeding(current_sentence_embbeding)

        # file generated only for tests:
        with open("sentences_embbedings_attribute.txt", 'a+', encoding="utf-8") as f:
            print(filtered_sentence.sentence_embbeding, file=f)

      
 
def ordering_by_similarity(sentence_candidates):

    '''
    Function that order the FIlteredSentence objects in descending
    order, according to its sentence score value.

    Parameters:

        sentence_candidates (list): contains FilteredSentences objects
    
    Returns:

        high_score_sentences(list): contains FilteredSentences objects
                                    ordered by its score value
                                    
    '''
    # order dict by items
    score_dict = {}
    for sentence in sentence_candidates:

        score_dict[sentence.score] = sentence


    score_dict_items = score_dict.items()
    sorted_score_list = sorted(score_dict_items)
    # sorted_score_list is a list containing a tuple: (score value, respective FilteredSentence)

    high_scores_sentences = []

    for sentence in sorted_score_list:

        high_scores_sentences.append(sentence[1])

    # list containing FilteredSentence objects already ordered by their similarity scores:
    return high_scores_sentences
    

   

    

def sentence_selection(sorted_sentences_by_score, discard_threshold, number_of_sentences_in_summary):
    
    '''
    Function that orders the FilteredSentence objects in descending
    order, according to its sentence score value.

    Parameters:

        sorted_sentences_by_score(list): contains FilteredSentences objects
                                    ordered by its score value
        discard_threshold (float): the threshold for cosine similarity,
                                   to discard sentences that are too similar
        number_of_sentences_in_summary(int): the number of desired sentneces in summary
    
    Returns:

        sentences_in_summary(list): list of FilteredSentences objects that were chosen 
                                    to compose the summary.
                                    
    '''

    sentences_in_summary = []
    # the FilteredSentence with the highest score is always selected:
    sentences_in_summary.append(sorted_sentences_by_score.pop(0))
    number_chosen_sentences = 1
    

    for candidate_sentence in sorted_sentences_by_score:
        print("analyzing the sentence: \n", candidate_sentence.raw_sentence)
        
        discard = False
        # comparing the similarity between the current analyzed sentence
        # with the others sentences already in summary:
        for chosen_sentence in sentences_in_summary:

            current_score = embbedings_utils.cosine_similarity(candidate_sentence.sentence_embbeding, chosen_sentence.sentence_embbeding)
            print("current score of sentences comparison: ", current_score)
            
            # if satisfied, the two sentences are too similar, and the
            # current sentnece must be discarded:
            if current_score >= discard_threshold:
                print("sentença descartada")
                discard = True
                break
            
        
        if not discard:

            print("sentence was appended")
            sentences_in_summary.append(candidate_sentence)
            number_chosen_sentences += 1
            
            if number_chosen_sentences >= number_of_sentences_in_summary:
                print("the number of desired sentences in the summary could be reached")
                return sentences_in_summary
    
    print("couldn't insert in summary the desired number of sentences")

    print("chosen sentences for summary: ", sentences_in_summary)
    return sentences_in_summary






def summary_string(sentences_in_summary, movie):
    '''
    Function that converts a FitleredSentence object
    in its string representation

    Parameters:

        sentences_in_summary(list): list of FilteredSentences objects that were chosen 
                                    to compose the summary.
        movie(Movie object): the current movie in the processing pipeline
                                    
    '''

    summary = ""
    for sentence_object in sentences_in_summary:
        
        summary += sentence_object.raw_sentence + "\n"

    print("summary: ", summary)
    return summary

        


    


            

