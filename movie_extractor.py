#código oficial, falta arrumar o sentence filtring (test_filtered_sentences.txt) acho que só flata complementar..nao arrumar!
import xml.etree.ElementTree as ET
import collections
import os 
import string
import Sentence 
import Review 
import Movie 


def movie_extractor(directory_path, aspects, set_of_movies, k):

    """
    Given the directory that contains xml files - each of them 
    representing a single review - this function instantiates movie
    objects. At the end of the function, it is computed the score of 
    each aspect belonging to the movie.

    Args:
        directory_path (str): the directory where the single reviews
        xml files are kept.

        aspects(dict): is a dict that maps each aspect to it's KL relevance
        number.

        set of movies(list): list containing the instantiated movie objects.

        k (int) : represents the number of the chosen main aspects (top k aspects)

        Returns:
            None.
    """

    for dirpath, dirnames, files in os.walk(directory_path):
        
        if dirpath[-4:] != "iews":

            new_movie = Movie.Movie(dirpath[-4:])

            for file in files:
                file_name = os.path.join(dirpath, file)
                new_review = Review.Review(file_name)
                new_review.review_extractor(aspects)
                #new_review.review_extractor(aspects)
                new_movie.reviews.append(new_review)
                new_movie.number_of_reviews += 1

            for review in new_movie.reviews:
                #aspects_in_review is a counter; it contains
                #the counting of aspects in the current review:
                aspects_in_review = review.occurrences_of_each_aspect

                #the above loop iterates through each aspect
                #belonging to the counter attribute ("aspects_in_review") of the review:
                for current_aspect in aspects_in_review:
                    #the counter "aspects_in_review" is acessed;
                    #the number of occurences of the "current_aspect" is 
                    #attritbuted to "current_aspect_count":

                    current_aspect_count = aspects_in_review[current_aspect]

                    #the KL value of the "current_aspect" is acessed
                    #in the dict of aspects:
                    aspect_KL_rel = aspects[current_aspect]
                    review_sent = review.average_sentiment

                    current_aspect_score = current_aspect_count * aspect_KL_rel * review_sent

                    if current_aspect == "film":
                        with open("debug_score"+ new_movie.xml + ".txt",'a+', encoding="utf-8") as f:
                            print(current_aspect, file=f)
                            print("current_aspect_count: ", current_aspect_count, file=f)
                            print("aspect_KL_rel: ", aspect_KL_rel, file=f)
                            print("review_sent: ", review_sent, file=f)
                            print("current_aspect_score: ", current_aspect_score, file=f)
                            print("new_movie.number_of_reviews: ", new_movie.number_of_reviews, file=f)
                            print("------------", file=f)

                    current_aspect_score = current_aspect_score / new_movie.number_of_reviews

                    #total = new_movie.temp_acumulator_aspect[current_aspect] + current_aspect_score

                    if current_aspect not in list(new_movie.aspects_score.keys()):
                        new_movie.aspects_score[current_aspect] = 0

                    score_acumulator = new_movie.aspects_score[current_aspect] + current_aspect_score

                    new_movie.aspects_score[current_aspect] = score_acumulator

            new_movie.top_k_aspects_evaluation(k)
            print(new_movie.aspects_score["film"])
            set_of_movies.append(new_movie)


def test_movie_extractor(set_of_movies):

    for movie in set_of_movies:
        file_destiny = "test_movie_extractor" + movie.xml + ".txt"
        #file_destiny = "batata" + movie.xml + ".txt"
        
        with open(file_destiny,'a+', encoding="utf-8") as f:
            print("#################################### Beggining of this movie ##########################\n", file=f)
            print("this movie belongs to the file: ",movie.xml, file=f)
            print("\nnumber of reviews of this movie: ", movie.number_of_reviews, file=f)
            print("\nScore of each aspect:", file=f)

            for aspect in movie.aspects_score:
                print("\taspect", aspect, ":", movie.aspects_score[aspect], file=f)

            print("\nTop-" + str(k) + " aspects:", file=f)

            for main_aspect in movie.top_k_aspects:
                print("\tmain aspect: ", main_aspect, file=f)

            print("\n", file=f)

            iterator = 1

            for review in movie.reviews:
                print("\n\tReview " + str(iterator) + ":", file=f)
                print("\n\t\tThis review belongs to the file: ", review.xml_name, file=f)
                print("\t\tAverage sentiment of this review: ", review.average_sentiment, file=f)
                print("\t\tNumber of sentences in this review: ", review.number_of_sentences, file=f)
                print("\t\tAspects and it's occurrence in this review: ", file=f)
                
                for aspect in review.occurrences_of_each_aspect:
                    print("\t\t\taspect: ", aspect," number of occurrences: ", review.occurrences_of_each_aspect[aspect], file=f)

                print("\n\t\t\t\t---sentences in this review ---\n", file=f)

                sentence_iterator = 1

                for sentence in review.sentences:
                    print("\t\t\t\tSentence " + str(sentence_iterator) + ":\n", file=f)
                    print("\t\t\t\tNumber of tokens in this sentence: ",sentence.number_of_tokens, file=f)
                    print("\t\t\t\tSentiment value of this sentence: ", sentence.sentiment_value, file=f)
                    
                    print("\t\t\t\tAspects in this sentence: ", file=f)
                    for aspect in sentence.aspects:
                        print("\t\t\t\t\t-", aspect, file=f)

                    print("\n\t\t\t\t\t" + sentence.__str__(), file=f)

                    print("\t\t\t\t------------------------------------------------\n", file=f)

                    sentence_iterator += 1

                print("\n\t\t**************************** end of this review **********************************", file=f)
               
                iterator +=1

            print("\n#################################### end of this movie ##########################\n", file=f)

'''def test_directory(directory_path):
    with open("test_directory.txt", 'a+', encoding="utf-8") as f:
        for dirpath, dirnames, files in os.walk(directory_path):
            #print("dirpath: ", dirpath, file=f)
            for file in files:
                filename = os.path.join(dirpath, file)
                print("filename: ", filename, file=f)
'''
def test_sentence_filtering(set_of_movies):

        for movie in set_of_movies:
            print(movie.xml)
            movie.sentence_filtering()

            with open("test_sentence_filtering.txt", 'a+', encoding="utf-8") as f:
                print("############ MOVIE: " + movie.xml + " ###########", file=f)

                for sentence in movie.filtered_sentences:

                    print("\n\t-------------- in movie "+ movie.xml +"-------------------", file=f)
                    print("\n\tSentence sentiment: ", sentence.sentiment, file=f)
                    print("\n\tSentence sentiment_value:", sentence.sentiment_value, file=f)
                    print("\n\tSentence number of tokens: ", sentence.number_of_tokens, file=f)
                    print("\n\tSentence personal opinion: ", sentence.personal_opinion, file=f)
                    print("\t\t\t\tAspects in this sentence: ", file=f)
                        
                    for aspect in sentence.aspects:
                        print("\t\t\t\t\t-", aspect, file=f)

                    print("\n\t\t\t\t\t" + sentence.__str__() + "\n", file=f)
            

    

if __name__ == '__main__':

    directory_path = "C:\\Users\\User\\Desktop\\ic\\single_xml_reviews"

    set_of_movies = []

    aspects = {'morality': 2, 'film': 3, 'dog': 5, 'movie': 7, 'art': 9, 'mother': 10, 'way': 11}

    k = 2

    movie_extractor(directory_path, aspects, set_of_movies, k)

    test_movie_extractor(set_of_movies)
    test_sentence_filtering(set_of_movies)
    #test_directory(directory_path)