import KL_divergence
import Movie
from pathlib import Path
import BNC_corpora_utilities 
import numpy as np
import time
import summarizer_pipeline
import babelsynsets_utils
import single_reviews_corenlp


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

        # computing the nouns that are going to be classified as aspects:
        new_movie.aspects_score = KL_divergence.epsilon_aspects_extraction(new_movie.KL_nouns_values, KL_threshold)
        
        # evaluation of the top-k aspects of the item:
        new_movie.top_k_aspects_evaluation(top_k_number)
        print("top-k aspects were evaluated.")
        
        # start the sentence filtering phase:
        new_movie.sentence_filtering()
        print("end of filtering sentence.")

        
        summary = summarizer_pipeline.summarizer_pipeline(disambiguation, 
                                                new_movie, 
                                                tf_idf_threshold, 
                                                babelfy_API_key,
                                                discard_threshold, 
                                                number_of_sentences_in_summary)

        filename = new_movie.xml_name + "_summary.txt"
        
        # the desired parameters and corresponding summarization are going to 
        # be printed in a .txt file:
        with open(filename, "a+", encoding="utf-8") as f:
            print("summarization for movie: ", new_movie.xml_name, file=f)
            print("disamgiguation: ", disambiguation, file=f)
            print("KL threshold: ", KL_threshold, file=f)
            print("top-k aspects: ", top_k_number, file=f)
            print("tf_idf_threshold: ", tf_idf_threshold, file=f)
            print("discard threshold: ", discard_threshold, file=f)
            print("number of sentences in summary: ", number_of_sentences_in_summary, file=f)
            print("\n\t",summary, file=f)
            print("****************************************************************************\n", file=f)
        

if __name__ == '__main__':


    # if you don't have BNC_nouns.db, set to "True":
    # (see README for more details)
    generate_BNC_db = False

    
    # if you don't have 'nouns_synsets_optimized.db', set to "True":
    # see README for more details
    generate_babelsynsets_dimensions_db = False

    #if you dont have reviews of an item parsed by CoreNLP, set to "True":
    # (see in the README the conditions to adapt your dataset)
    generate_single_corenlp_reviews = False
    
    # if disambiguation is desired, set to "True".
    # disambiguation improves the results, so setting it to "True" is generally desired.
    disambiguation = True

    # the KL_threshold described in the paper to classify a noun as an aspect:
    KL_threshold = -20

    # top_k_number: the number of "top_k" aspects ranked; as an example, if top_k_number = 5,
    # the top-5 aspects of an item are selected
    top_k_number = 50

    # in the summarization phase, the sentences having a tf_idf value greater
    # than a certain threshold are included in the centroid embbeding construction:
    tf_idf_threshold = 0.35

    # babelfy_API_key is your key to acces the Babelfy services.
    # you should register to obtain a key. You have a limited
    # number of babelcoins daily.

    babelfy_API_key = 'insert your babelfy API key here'

    # the similarity to discard a sentence to be included in the summary,
    # to avoid redundancy:
    discard_threshold = 0.65

    # number of the desired sentences to be in the summary:
    number_of_sentences_in_summary = 10

    if generate_BNC_db:

        parsed_tokens = BNC_corpora_utilities.extract_BNC_nouns()
        BNC_corpora_utilities.create_BNC_frequency_files(parsed_tokens)
        BNC_corpora_utilities.create_db()

    if generate_babelsynsets_dimensions_db:

        babelsynsets_utils.create_synsets_db_optimized()

    if generate_single_corenlp_reviews:
        single_reviews_corenlp.arsing_reviews_corenlp()


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
