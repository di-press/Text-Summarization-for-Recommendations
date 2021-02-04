import KL_divergence
import Movie
from pathlib import Path
import BNC_corpora_utilities 
import numpy as np
import time
import summarizer_pipeline


def paper_pipeline(KL_threshold, 
                        top_k_number,  
                        generate_BNC_db, 
                        generate_single_corenlp_reviews,
                        disambiguation, 
                        tf_idf_threshold,
                        babelfy_API_key, 
                        discard_threshold, 
                        number_of_sentences_in_summary):

    current_directory = Path.cwd()

    movies_directory = Path(current_directory, "single_reviews_corenlp")
       
    for single_movie_directory in movies_directory.iterdir():

        print("trying to create: ", single_movie_directory)
        new_movie = Movie.Movie(single_movie_directory)
        print("movie created:", new_movie.xml_name)
        new_movie.KL_values()

        new_movie.aspects_score = KL_divergence.epsilon_aspects_extraction(new_movie.KL_nouns_values, KL_threshold)
        new_movie.top_k_aspects_evaluation(top_k_number)
        print("top-k aspects were evaluated.")
        new_movie.sentence_filtering()
        print("end of filtering sentence.")

        
        summarizer_pipeline.summarizer_pipeline(disambiguation, 
                                                new_movie, 
                                                tf_idf_threshold, 
                                                babelfy_API_key,
                                                discard_threshold, 
                                                number_of_sentences_in_summary)
        

if __name__ == '__main__':


    # if you don't have BNC_nouns.db, set to "True":
    generate_BNC_db = False
    
    #if you dont have reviews of an item parsed by CoreNLP, set to "True":
    # (see in the README the conditions to adapt your dataset)
    generate_single_corenlp_reviews = False
    
    # if disambiguation is desired, set to "True".
    # disambiguation improves the results, so setting it to "True" is generally desired.
    disambiguation = True

    # the KL_threshold described in the paper to classify a noun as an aspect:
    KL_threshold = -50

    # top_k_number: the number of "top_k" aspects ranked; as an example, if top_k_number = 5,
    # the top-5 aspects of an item are selected
    top_k_number = 50

    # in the summarization phase, the sentences having a tf_idf value greater
    # than a certain threshold are included in the centroid embbeding construction:
    tf_idf_threshold = 0.2

    # babelfy_API_key is your key to acces the Babelfy services.
    # you should register to obtain a key. You have a limited
    # number of babelcoins daily.
    babelfy_API_key = 'insert your API key here'

    # the similarity to discard a sentence to be included in the summary,
    # to avoid redundancy:
    discard_threshold = 0.8

    # number of the desired sentences to be in the summary:
    number_of_sentences_in_summary = 6

    start = time.perf_counter()

    # function that covers all the pipeline described in the paper:
    paper_pipeline(KL_threshold, 
                    top_k_number, 
                    generate_BNC_db, 
                    generate_single_corenlp_reviews, 
                    disambiguation, 
                    tf_idf_threshold,
                    babelfy_API_key,
                    discard_threshold,
                    number_of_sentences_in_summary)

    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)
