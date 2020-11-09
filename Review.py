import Sentence as Sentence
import os
from collections import Counter
import xml.etree.ElementTree as ET
import collections
from itertools import chain 
import string


class Review:
    def __init__(self, xml_name):
        self._xml_name = xml_name
        self._sentences = []
        self._number_of_sentences = 0
        self._occurrences_of_each_aspect = Counter()
        self._aspects = []
        self._average_sentiment = 0
        

    @property
    def sentences(self):
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


    def review_test(self, file_destiny):
        with open(file_destiny, 'a', encoding="utf-8") as f:
            print("\tThis review belongs to the file: ", self._xml_name, file=f)
            print("\tAverage sentiment of this review: ", self._average_sentiment, file=f)
            print("\tNumber of sentences in this review: ", self._number_of_sentences, file=f)
            print("\tAspects and it's occurrence in this review: ", file=f)
            
            for aspect in self._occurrences_of_each_aspect:
                print("aspect: ", aspect," number of occurrences: ", self.occurrences_of_each_aspect[aspect], file=f)

            print("\n---sentences in this review ---\n", file=f)

            for sentence in self._sentences:
                print("\t\tNumber of tokens in this sentence: ",sentence.number_of_tokens, file=f)
                print("\t\tSentiment value of this sentence: ", sentence.sentiment_value, file=f)
                print("\t\tPersonal opinions in this sentence: ", sentence.personal_opinion, file=f)

                print("\t\tAspects in this sentence: ", file=f)
                for aspect in sentence.aspects:
                    print("\t\t\t-", aspect, file=f)

                print(sentence.__str__(), file=f)

                print("---------------------------------------------------------", file=f)

            print("******************************* end of this review **********************************", file=f)

     
        
    def review_extractor(self, aspects): 
        """
        Given a xml file that represents a review, this function instantiates 
        review objects (and consequently, sentence objects) by parsing the xml tree.
        For each review object, is computed it's xml name, it's sentences, number of sentences,
        average sentiment, list of aspects and the number of the occurrences of each aspect.
        The aspects are stored in lower case.


        
        Args: 
            aspects (dict): a dict contianing the aspects in lower case extracted by
            the function epsilon_aspects_extraction in KL_divergence.py

        Returns:
            A instantiate review object.

        """    
        aspects = list(aspects.keys())

        #new_review = Review(xml_name)
        xml_name = self.xml_name
        
        #https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        #PRP: Personal pronoun
        #PRP$	Possessive pronoun
        desired_POS = ["PRP", "PRP$"]

        #first person pronouns should be compared in lower case:
        first_person_pronoun = ["i","we", "us","me","my","mine", "our", "ours"]
        #myself and ourselves??(reflexive pronoun)

        tree = ET.parse(xml_name)
        root = tree.getroot()

        element = root.findall(".//sentence")# finds only elements with the tag "sentence" which are direct children of the current root    

        punctuation = [i for i in string.punctuation]

        for sentence in element:
            word_counter = 0
            id = sentence.attrib["id"]
            sentiment_value = sentence.attrib["sentimentValue"]
            sentiment = sentence.attrib["sentiment"]
            new_sentence = Sentence.Sentence(id, sentiment_value, sentiment, xml_name)
            self._number_of_sentences += 1
            sentiment_value = int(sentiment_value)            
            self._average_sentiment += sentiment_value
            
            
            sentence.findall(".//token")

            for tokens in sentence:
                for token in tokens:

                    for token_child in token:

                        if token_child.tag == "word":
                            current_word = token_child.text.lower()

                            if current_word in first_person_pronoun:
                                #print(current_word)
                                #personal opinion is setted to True:
                                new_sentence.personal_opinion = True

                            new_sentence.add_token(token_child.text) 

                            if token_child.text.lower() in aspects:
                                new_sentence.add_aspect(token_child.text.lower())  
                                self._aspects.append(token_child.text.lower())

                            if token_child.text not in punctuation:
                                word_counter += 1

            new_sentence.number_of_tokens = word_counter
            self._sentences.append(new_sentence)

        self._average_sentiment = self._average_sentiment / self._number_of_sentences
        self._occurrences_of_each_aspect = Counter(self._aspects)
        
            

if __name__ == '__main__':

    aspects = {'morality': 2, 'film': 3, 'dog': 5, 'movie': 7, 'art': 9, 'mother': 10, 'way': 11}
    #new_review = Review.review_extractor("x2145_1.xml", aspects)
    #new_review.review_test("Reviewx2145_1.txt")

    new_review = Review("x2145_1.xml")
    new_review.review_extractor(aspects)
    new_review.review_test("Review3.txt")