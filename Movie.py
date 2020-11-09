from collections import Counter
import Sentence as Sentence
import Review as Review

class Movie:

    def __init__(self, xml):

        self.xml = xml
        self.reviews = []
        self.number_of_reviews = 0
        self.aspects_score = {}
        self.top_k_aspects = []
        self.filtered_sentences = []

    def top_k_aspects_evaluation(self, k):
        #above, key=lambda x: x[1] guarantees that the dict is going to be sorted by 
        #it's score value;
        #reverse=True means the ordering is going to be in descending order
        sorted_aspects = sorted(self.aspects_score.items(), key=lambda x: x[1], reverse=True)
       
        for x in sorted_aspects[0:k]:
            self.top_k_aspects.append(x[0])


    def sentence_filtering(self):
        for review in self.reviews:

            for sentence in review.sentences:
                counter_of_aspects = Counter(sentence.aspects)

                for aspect in counter_of_aspects:
                   # number of tokens bigger than 5, non personal pronouns, and positive sentiment value;
                    if aspect in self.top_k_aspects:
                        if sentence.number_of_tokens > 5 and int(sentence.sentiment_value) >= 3 :
                            if not sentence.personal_opinion:                                  
                                self.filtered_sentences.append(sentence)

    
    