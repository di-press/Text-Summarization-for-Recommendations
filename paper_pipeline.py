#import BNC_nouns_extractor
#import reviews_noun_extractor
#import counter_occurrences
import KL_divergence
import Movie
from pathlib import Path
import BNC_corpora_utilities 
import numpy as np
#import movie_extractor 


def paper_pipeline(KL_threshold, top_k_number):

    current_directory = Path.cwd()

    movies_directory = Path(current_directory, "single_reviews_corenlp")
       
    for single_movie_directory in movies_directory.iterdir():

        new_movie = Movie.Movie(single_movie_directory)
        print("movie created:", new_movie.xml_name)
        new_movie.KL_values()

        new_movie.aspects_score = KL_divergence.epsilon_aspects_extraction(new_movie.KL_nouns_values, KL_threshold)
        new_movie.top_k_aspects_evaluation(top_k_number)
        new_movie.sentence_filtering()
        
        print(new_movie.filtered_sentences)

        

if __name__ == '__main__':

# corenlp reviews parsing
# db creation

    paper_pipeline(KL_threshold=-20, top_k_number=20)
