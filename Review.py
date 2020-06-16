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
        #self._review_representation = review_representation

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
    

    def review_extractor(xml_name, aspects): #aspects is a dict of aspects already extracted
    
        aspects = list(aspects.keys())

        new_review = Review(xml_name)
        
        tree = ET.parse(xml_name)
        root = tree.getroot()

        element = root.findall(".//sentence")# finds only elements with the tag "sentence" which are direct children of the current root    

        #parsed_reviews=[]
        punctuation = [i for i in string.punctuation]

        for sentence in element:
            word_counter = 0
            id = sentence.attrib["id"]
            sentiment_value = sentence.attrib["sentimentValue"]
            sentiment = sentence.attrib["sentiment"]
            new_sentence = Sentence.Sentence(id, sentiment_value, sentiment, xml_name)
            new_review._number_of_sentences += 1
            new_review._average_sentiment += sentiment_value
            
            
            sentence.findall(".//token")

            for tokens in sentence:
                for token in tokens:

                    for token_child in token:
                        if token_child.tag == "word":

                            new_sentence.add_token(token_child.text) 

                            if token_child.text.lower() in aspects:
                                new_sentence.add_aspect(token_child.text.lower())  
                                new_review._aspects.append(token_child.text.lower())

                            if token_child.text not in punctuation:
                                word_counter += 1

            new_sentence.number_of_tokens = word_counter
            new_review._sentences.append(new_sentence)

            return new_review
        
        

            '''with open(file_destiny, 'a+', encoding="utf-8") as f:
                print("This sentence is in the file: ", new_sentence.xml, file=f)
                print("Id sentence: ", new_sentence.id_sentence, file=f)
                print("Sentiment value of the sentence: ", new_sentence.sentiment_value, file=f)
                print("Sentiment of the sentence: ", new_sentence.sentiment, file=f)
                
                print("Aspects: ", file=f)
                for aspect in new_sentence.aspects:
                    print(aspect, file=f)

                print("\nNumber of tokens in this sentence: ", new_sentence.number_of_tokens, file=f)
                print("Tokens in this sentence: ", file=f)
                print(new_sentence.__str__(), file=f)

                print("\n ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n", file=f)
            '''

        new_review._average_sentiment = new_review._average_sentiment / new_review._number_of_sentences
        new_review._occurrences_of_each_aspect = Counter(new_review._aspects)

