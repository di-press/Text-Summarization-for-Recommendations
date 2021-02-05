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
    
    print("started centroid construction")
    centroid = centroid_pipeline(disambiguation, movie, tf_idf_threshold, babelfy_API_key)


    with open("centroid_no_disambiguation.txt", 'a+', encoding='utf-8') as f:
        print(centroid, file=f)
     
    id = 0
    sentence_candidates = []
    for filtered_sentence in movie.filtered_sentences:

        current_sentence = FilteredSentence.FilteredSentence(id, filtered_sentence)
        sentence_candidates.append(current_sentence)
        id += 1

        with open("filtered_sentences_instantiaton.txt", 'a+', encoding='utf-8') as f:
            print(sentence_candidates, file=f)
    
    sentence_embbedings_pipeline(disambiguation, sentence_candidates, babelfy_API_key)

    for filtered_sentence in sentence_candidates:

        score = embbedings_utils.cosine_similarity(centroid, filtered_sentence.sentence_embbeding)
        filtered_sentence.add_score(score)
    
    # sentence_candidates é uma lista com objetos filtered_sentences, já com o embbeding d cada sentença 
    # calculados. Falta o sentence scoring, sentence selection e tb ajustar pra qndo n se quer desambiguar
    sorted_sentences_by_score = ordering_by_similarity(sentence_candidates)

    sentences_in_summary = sentence_selection(sorted_sentences_by_score, discard_threshold, number_of_sentences_in_summary)

    summary = summary_string(sentences_in_summary, movie)
    
    return summary


def centroid_pipeline(disambiguation, movie, tf_idf_threshold, babelfy_API_key):

    if disambiguation:
        print("started disambiguation.")
        disambiguator.disambiguate_raw_reviews(movie.reviews, babelfy_API_key)
    # else: find the synset in dbsearch_in_synsets_db

        babelsynsets_documents = []

        for review in movie.reviews:
            
            #print("review.nouns_and_babelsynsets: ", review.nouns_and_babelsynsets)
            current_review_document = ""
            for pair in review.nouns_and_babelsynsets:
                #print("pair[1]: ", pair[1])
                current_review_document += pair[1] + " "
            
            babelsynsets_documents.append(current_review_document)
            
            #with open("teste_reviews_disambiguating.txt", 'a+', encoding='utf-8') as f:
                #print(review.nouns_and_babelsynsets, file=f)
        
        #print(babelsynsets_documents)
        print("started tf_idf selection")
        
        selected_tf_idf_synsets = tf_idf.tf_idf_centroid_selection(babelsynsets_documents, tf_idf_threshold) 

        print("selected synsets from tf-idf")
        #print(selected_tf_idf_words)


        selected_tf_idf_dimensions = babelsynsets_utils.search_in_synsets_db_optimized(selected_tf_idf_synsets) 
        print("going to centroid phase")
        centroid = embbedings_utils.centroid_construction(selected_tf_idf_dimensions)
    # if disambiguation is not desired:
    else:

        documents_for_tf_idf = []

        for review in movie.reviews:

            processed_review = strip_punctuation(review.raw_review)
            processed_review = remove_stopwords(processed_review)
            # now, processed review is a document going to tf-idf phase

            documents_for_tf_idf.append(processed_review)
        print("started tf_idf selection")
        
        selected_tf_idf_words = tf_idf.tf_idf_centroid_selection(documents_for_tf_idf, tf_idf_threshold)

        print("selected words from tf-idf")
        synsets_to_search = no_disambiguation.process_raw_reviews(selected_tf_idf_words, babelfy_API_key)
        
        selected_tf_idf_dimensions = babelsynsets_utils.search_in_synsets_db_optimized(synsets_to_search) 
        
        print("going to centroid phase")
        centroid = embbedings_utils.centroid_construction(selected_tf_idf_dimensions)

    return centroid




def sentence_embbedings_pipeline(disambiguation, sentence_candidates, babelfy_API_key):
    
    if disambiguation:
        
        print("started filtered sentences embbedings construction with disambiguation.")
        disambiguator.disambiguate_filtered_sentence(sentence_candidates, babelfy_API_key)

    else:
        print("started filtered sentences embbedings construction.")
        no_disambiguation.process_filtered_sentences(sentence_candidates, babelfy_API_key)
    
    for filtered_sentence in sentence_candidates:
        
        filtered_sentence_babelsynset = []

        for pair in filtered_sentence.babelsynsets_words:
            filtered_sentence_babelsynset.append(pair[1])
        
        
        babelsynsets_dimensions = babelsynsets_utils.search_in_synsets_db_optimized(filtered_sentence_babelsynset)

        current_sentence_embbeding = embbedings_utils.filtered_sentence_embbeding(babelsynsets_dimensions)
        
        filtered_sentence.add_sentence_embbeding(current_sentence_embbeding)

        with open("sentences_embbedings_attribute.txt", 'a+', encoding="utf-8") as f:
            print(filtered_sentence.sentence_embbeding, file=f)

      
 
def ordering_by_similarity(sentence_candidates):
    # order dict by items
    score_dict = {}
    for sentence in sentence_candidates:

        #print(sentence.score)
        score_dict[sentence.score] = sentence


    score_dict_items = score_dict.items()
    sorted_score_list = sorted(score_dict_items)

    high_scores_sentences = []
    #teste = []

    for sentence in sorted_score_list:

        high_scores_sentences.append(sentence[1])
        #teste.append(sentence)
    
    #print("lista com scores ordenados: ", teste)
    # list containing sentnece objects already ordered by theysimilarity scores:
    return high_scores_sentences
    

   

    

def sentence_selection(sorted_sentences_by_score, discard_threshold, number_of_sentences_in_summary):

    sentences_in_summary = []
    print("numero sentenças iniciais: ", len(sorted_sentences_by_score))

    sentences_in_summary.append(sorted_sentences_by_score.pop(0))
    number_chosen_sentences = 1
    
    #print("candidate sentences: ", sorted_sentences_by_score)

    for candidate_sentence in sorted_sentences_by_score:
        print("analisando a sentença: \n", candidate_sentence.raw_sentence)
        
        discard = False
        for chosen_sentence in sentences_in_summary:

            current_score = embbedings_utils.cosine_similarity(candidate_sentence.sentence_embbeding, chosen_sentence.sentence_embbeding)
            print("current score of sentences comparison: ", current_score)
            
            if current_score >= discard_threshold:
                print("sentença descartada")
                discard = True
                break
            
            if current_score == np.nan:
                print("zero")
                discard = True
                break
        
        if not discard:

            print("sentence was appended")
            sentences_in_summary.append(candidate_sentence)
            number_chosen_sentences += 1
            
            if number_chosen_sentences >= number_of_sentences_in_summary:
                print("chegou em 10 sentneças")
                return sentences_in_summary
    
    print("couldn't insert in summary the desired number of sentences")

    print("chosen sentences for summary: ", sentences_in_summary)
    return sentences_in_summary






def summary_string(sentences_in_summary, movie):


    summary = ""
    for sentence_object in sentences_in_summary:
        
        summary += sentence_object.raw_sentence + "\n"

    print("summary: ", summary)
    return summary

        


    


            

