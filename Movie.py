from collections import Counter
import Sentence as Sentence
import Review as Review
from pathlib import Path
import BNC_corpora_utilities 
import KL_divergence 


class Movie:

    def __init__(self, single_movie_directory):

        self.xml_name = single_movie_directory.name
        self.reviews = []
        self.number_of_reviews = 0
        self.aspects_score = {}
        self.top_k_aspects = []
        self.filtered_sentences = []
        self.nouns_occurrences = Counter() 
        self.KL_nouns_values = {}

        self.movie_extractor(single_movie_directory)


    
    def movie_extractor(self, single_movie_directory):

        for filename in single_movie_directory.iterdir():
            
            new_review = Review.Review(filename)
            
            if new_review:
                
                self.reviews.append(new_review)
                self.number_of_reviews += 1
                new_review.id = self.number_of_reviews
                
                for noun in new_review.nouns_occurrences:
                    self.nouns_occurrences[noun] += new_review.nouns_occurrences[noun] 


    
    def KL_values(self):

        nouns_frequencies_in_corporas = BNC_corpora_utilities.search_noun_BNC_db(self.nouns_occurrences)

        for noun_values in nouns_frequencies_in_corporas:

            noun = noun_values[0]
            frequency_in_reviews = noun_values[1]
            frequency_in_BNC = noun_values[2]      

            noun_KL_value = KL_divergence.KL_divergence(frequency_in_reviews, frequency_in_BNC)

            self.KL_nouns_values[noun] = noun_KL_value

            


    def top_k_aspects_evaluation(self, k):
        #above, key=lambda x: x[1] guarantees that the dict is going to be sorted by 
        #it's score value;
        #reverse=True means the ordering is going to be in descending order
        sorted_aspects = sorted(self.aspects_score.items(), key=lambda x: x[1], reverse=True)
       
        for x in sorted_aspects[0:k]:
            self.top_k_aspects.append(x[0])

   
    
    def aspect_scoring(self):

        for aspect in self.aspects_score:

            accumulated_score = 0

            for review in self.reviews:

                accumulated_score = review.nouns_occurrences[aspect] * KL_nouns_values[aspect] * review.average_sentiment

            aspect_score = accumulated_score / self.number_of_reviews
            
            self.aspects_score[aspect] = aspect_score

    
    
    def sentence_filtering(self):
        
        for review in self.reviews:

            for sentence in review.sentences:
                if not sentence.personal_opinion:
                    if sentence.number_of_tokens > 5 and int(sentence.sentiment_value) >= 3: 

                        nouns_in_sentence = sentence.retrieve_nouns()
                        
                        for noun in nouns_in_sentence.keys():
                            if noun in self.top_k_aspects:
                                self.filtered_sentences.append(sentence.__str__())



    def movie_instantiating_test(self):

        print("processing nouns of movie")
        print("finish processing nouns")

        with open("movie_instantiating_test3.txt", "a+", encoding="utf-8") as f:

            print("movie name: ", self.xml_name, file=f)
            print("number of reviews: ", self.number_of_reviews, file=f)
            print("nouns occurrences: ", self.nouns_occurrences, file=f)
            print("\t(noun in this movie, occurrences in movie, occurrences in BNC)", file=f)
            print("reviews information: ", file=f)



            for review in self.reviews:
                print("\treview id = ", review.id, file=f)
                print("\traw review = ", review.raw_review, file=f)
                print("\taverage sentiment = ", review.average_sentiment, file=f)




    def search_noun_BNC_db_test(self):

        nouns_values_list = BNC_corpora_utilities.search_noun_BNC_db(self.nouns_occurrences)

        print(nouns_values_list)   

    
if __name__ == '__main__':

    
    current_directory = Path.cwd()

    movies_directory = Path(current_directory, "single_reviews_corenlp")
    
    

    for single_movie_directory in movies_directory.iterdir():

        new_movie = Movie(single_movie_directory)
        new_movie.movie_instantiating_test()
        new_movie.search_noun_BNC_db_test()


        
