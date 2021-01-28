import KL_divergence
import Movie
from pathlib import Path
#import BNC_corpora_utilities 
import numpy as np
import time



def paper_pipeline(KL_threshold, top_k_number, generate_BNC_db, generate_single_corenlp_reviews):

    '''
        This function follows the logical pipeline described in the paper for each item (movie).
        It produces the final summarization for each desired item.
    '''

    current_directory = Path.cwd()
    # single_reviews_corenlp is a directory containing other folders inside it, in which
    # there are .txt files representing the item reviews
    movies_directory = Path(current_directory, "single_reviews_corenlp")
       
    for single_movie_directory in movies_directory.iterdir():

        print("trying to create: ", single_movie_directory)
        new_movie = Movie.Movie(single_movie_directory)
        print("movie created:", new_movie.xml_name)
        new_movie.KL_values()

        new_movie.aspects_score = KL_divergence.epsilon_aspects_extraction(new_movie.KL_nouns_values, KL_threshold)
        # above, the top k aspects of a given itme is evaluated:
        new_movie.top_k_aspects_evaluation(top_k_number)
        # in the sentence filtering phase, the sentences there are going to feed the
        # summarizator are selected:
        new_movie.sentence_filtering()

        with open("filtered_sentences_test.txt", 'a+', encoding="utf-8") as f:
   
                print(new_movie.filtered_sentences, file=f)

        

if __name__ == '__main__':


    KL_threshold=-20
    # top_k_number: the number of "top_k" aspects ranked; as an example, if top_k_number = 5,
    # the top-5 aspects of an item are selected
    top_k_number=20

    # if you don't have the BNC_nouns.db, set to True:
    generate_BNC_db = False

    # if you have the dataset, or want to adapt yours under certain conditions described in the README,
    # set to True:
    generate_single_corenlp_reviews = False

    start = time.perf_counter()
    # all the paper pipeline is rpresented in this function:
    paper_pipeline(KL_threshold, top_k_number, generate_BNC_db, generate_single_corenlp_reviews)


    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)
