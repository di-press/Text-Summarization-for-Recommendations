import Sentence as Sentence
import Review as Review

class Movie:

    def __init__(self, xml):

        self.xml = xml
        self.reviews = []
        self.number_of_reviews = 0
        self.aspects_score = {}
        #self.top_k_aspects = {}

    