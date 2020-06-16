import xml.etree.ElementTree as ET
import collections
import os 
import string
import Sentence as Sentence
import Review as Review


#aspects is a dict that maps each aspect to it's KL relevance
    def movie_extractor(directory_path, aspects, set_of_movies):
        
        basepath = directory_path

        for dirpath, dirnames, files in os.walk(basepath):
            
            new_movie.Movie(dirpath[-4:])
            #print(f'Found directory: {dirpath}')
            for file_name in files:
                new_review = review_extractor(file_name, aspects)
                new_movie.reviews.append(new_review)
                new_movie.number_of_reviews += 1
                #print(file_name)

            for review in new_movie.reviews:
                aspects_in_review = review.occurrences_of_each_aspect()

                for current_aspect in aspects_in_review:

                    current_aspect_count = aspects_in_review[current_aspect]
                    aspect_KL_rel = aspects[current_aspect]
                    review_sent = review.average_sentiment()

                    current_aspect_score = current_aspect_count * aspect_KL_rel * review_sent

                    current_aspect_score = current_aspect_score / new_movie.number_of_reviews

                    new_movie.aspects_score[current_aspect] = current_aspect_score

            set_of_movies.append(new_movie)


if __name__ == '__main__':
    directory_path = "C:\\Users\\User\\Desktop\\ic\\xml_reviews"

    new_movie = Movie("")

    new_movie.movie_extractor(directory_path)