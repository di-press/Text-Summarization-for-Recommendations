#import BNC_nouns_extractor
#import reviews_noun_extractor
#import counter_occurrences
import KL_divergence
import Movie
from pathlib import Path
import BNC_corpora_utilities 
import numpy as np
import time
#import movie_extractor 


def paper_pipeline(KL_threshold, top_k_number, generate_BNC_db, generate_single_corenlp_reviews):

    current_directory = Path.cwd()

    movies_directory = Path(current_directory, "single_reviews_corenlp")
       
    for single_movie_directory in movies_directory.iterdir():

        print("trying to create: ", single_movie_directory)
        new_movie = Movie.Movie(single_movie_directory)
        print("movie created:", new_movie.xml_name)
        new_movie.KL_values()

        new_movie.aspects_score = KL_divergence.epsilon_aspects_extraction(new_movie.KL_nouns_values, KL_threshold)
        new_movie.top_k_aspects_evaluation(top_k_number)
        new_movie.sentence_filtering()
        
        with open("teste_pasta.txt", 'a+', encoding="utf-8") as f:
   
                print(new_movie.filtered_sentences, file=f)

        

if __name__ == '__main__':


    KL_threshold=-20
    # top_k_number: the number of "top_k" aspects ranked; as an example, if top_k_number = 5,
    # the top-5 aspects of an item are selected
    top_k_number=20
    generate_BNC_db = False
    generate_single_corenlp_reviews = False

    start = time.perf_counter()
    paper_pipeline(KL_threshold, top_k_number, generate_BNC_db, generate_single_corenlp_reviews)


    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)
