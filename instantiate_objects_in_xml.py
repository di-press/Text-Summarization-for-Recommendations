# não vou usar mais esse módulo:
import xml.etree.ElementTree as ET
import collections
from itertools import chain
import os 
import string
import Sentence as Sentence

def sentence_extractor(xml_name, aspects, file_destiny): #aspects is a dict of aspects already extracted
    
    aspects = list(aspects.keys())
    
    tree = ET.parse(xml_name)
    root = tree.getroot()

    element = root.findall(".//sentence")# finds only elements with the tag "sentence" which are direct children of the current root    

    parsed_reviews=[]
    punctuation = [i for i in string.punctuation]

    for sentence in element:
        word_counter = 0
        id = sentence.attrib["id"]
        sentiment_value = sentence.attrib["sentimentValue"]
        sentiment = sentence.attrib["sentiment"]
        new_sentence = Sentence.Sentence(id, sentiment_value, sentiment, xml_name)
          
        sentence.findall(".//token")

        for tokens in sentence:
            for token in tokens:

                for token_child in token:
                    if token_child.tag == "word":

                        new_sentence.add_token(token_child.text) 

                        if token_child.text in aspects:
                            new_sentence.add_aspect(token_child.text.lower())  

                        if token_child.text not in punctuation:
                            word_counter += 1

        new_sentence.number_of_tokens = word_counter

        with open(file_destiny, 'a+', encoding="utf-8") as f:
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


if __name__ == '__main__':

    aspects = {'morality': 0, 'film': 1, 'dog': 2}
    #aspects_list = list(aspects_dict.keys())
    sentence_extractor("x2145_1.xml", aspects, "xml_parsados.txt")