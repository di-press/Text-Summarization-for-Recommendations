import Sentence as Sentence
import os
from collections import Counter
import xml.etree.ElementTree as ET
import collections
from itertools import chain 
import string
from pathlib import Path


class Review:
    def __init__(self, file):
        self._id = 0
        self._xml_name = "not instantiated yet"
        self._sentences = []
        self._number_of_sentences = 0
        self._occurrences_of_each_aspect = Counter()
        self._aspects = []
        self._average_sentiment = 0
        self._raw_review = ""
        self._nouns_occurrences = Counter()

        self.review_extractor(file)
        
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def sentences(self):
        '''
            Returns the list of Sentence objects in a Review
        '''
        return self._sentences
    
    @property
    def number_of_sentences(self):
        return self._number_of_sentences

    @number_of_sentences.setter
    def number_of_sentences(self, number):
        self._number_of_sentences = number

    @property
    def occurrences_of_each_aspect(self):
        return self._occurrences_of_each_aspect

    @property
    def average_sentiment(self):
        return self._average_sentiment

    @property
    def xml_name(self):
        return self._xml_name
    
    @property
    def nouns_occurrences(self):
        return self._nouns_occurrences

    @property
    def raw_review(self):
        return self._raw_review




    def review_extractor(self, file): 
        """
        Given a xml file that represents a review, this function instantiates 
        review objects (and consequently, sentence objects) by parsing the xml tree.
        For each review object, is computed it's xml name, it's sentences, number of sentences,
        average sentiment, and occurrences of nouns. The aspects aren't instantiated in
        this function, but in the module Movie.py.

        
        Args: 
            file (Path): the .xml file containing a raw single review

        Returns:
            None

        """    
        
        filename = file.name.split(".")
        filename = filename[0] + ".xml"

        self._xml_name = filename
        
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        # NN 	Noun, singular or mass
     	# NNS 	Noun, plural
     	# NNP 	Proper noun, singular
    	# NNPS 	Proper noun, plural
        
        desired_POS=["NN", "NNS", "NNP", "NNPS"]
       
        # first person pronouns are not desired in the sentences, since they can indicate a personal opinion.
        #first person pronouns should be compared in lower case:
        first_person_pronoun = ["i","we", "us","me","my","mine", "our", "ours", "myself", "ourselves"]
        

        tree = ET.parse(file)
        root = tree.getroot()

        # finds only elements with the tag "sentence" which are direct children of the current root    
        element = root.findall(".//sentence")

        # identifying punctuation characters:
        punctuation = [i for i in string.punctuation]

        for sentence in element:
            
            word_counter = 0

            id = sentence.attrib["id"]
            sentiment_value = sentence.attrib["sentimentValue"]
            sentiment = sentence.attrib["sentiment"]

            new_sentence = Sentence.Sentence(id, sentiment_value, sentiment, filename)
            self._number_of_sentences += 1

            sentiment_value = int(sentiment_value)            
            self._average_sentiment += sentiment_value
            
            # xml parsing:
            sentence.findall(".//token")

            for tokens in sentence:
                for token in tokens:

                    for token_child in token:

                        if token_child.tag == "word":

                            current_word = token_child.text.lower()

                            if current_word in first_person_pronoun:
                                #personal opinion is setted to True:
                                new_sentence.personal_opinion = True

                            new_sentence.add_token(token_child.text) 

                            if token_child.text not in punctuation:

                                word_counter += 1

                        if token_child.tag == "POS" and token_child.text in desired_POS:
                            # a noun was found in the xml tree:
                           
                            for token_child in token:
                                
                                if token_child.tag == "word":
                                    new_sentence.add_noun(token_child.text.lower())  
                                    self._nouns_occurrences[token_child.text.lower()] += 1
                                    

            new_sentence.number_of_tokens = word_counter
            self._sentences.append(new_sentence)
            self._raw_review += new_sentence.__str__()

        self._average_sentiment = self._average_sentiment / self._number_of_sentences

            

    def review_test(self, file_destiny):
        # mode a: only appending
        with open(file_destiny, 'a', encoding="utf-8") as f:
            print("\tRaw Review: ", self._raw_review, file=f)
            print("\tThis review belongs to the file: ", self._xml_name, file=f)
            print("\tAverage sentiment of this review: ", self._average_sentiment, file=f)
            print("\tNumber of sentences in this review: ", self._number_of_sentences, file=f)
            print("\tNouns in this review: ", self._nouns_occurrences, file=f)
            print("\n---sentences in this review ---\n", file=f)

            for sentence in self._sentences:
                print("\t\tNumber of tokens in this sentence: ",sentence.number_of_tokens, file=f)
                print("\t\tSentiment value of this sentence: ", sentence.sentiment_value, file=f)
                print("\t\tPersonal opinions in this sentence: ", sentence.personal_opinion, file=f)
                print("\t\t", sentence.__str__(), file=f)

                print("---------------------------------------------------------", file=f)

            print("******************************* end of this review **********************************", file=f)

     
        
    
# test for instantiating all the reviews in the "single_reviews_corenlp" folder
if __name__ == '__main__':


    current_directory = Path.cwd()
    
    movies_directory = Path(current_directory, "single_reviews_corenlp")

    for single_movie_directory in movies_directory.iterdir():
        
        for filename in single_movie_directory.iterdir():
            
            new_review = Review(filename)
            new_review.review_test("review_test.txt")

    