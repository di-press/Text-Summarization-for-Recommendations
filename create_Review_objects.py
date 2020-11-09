#guardar as reviews com sentimentos positivos e mto positivos
#ver se tem aspectos nessa review
#se tiver, contar o numero de ocorrencias do aspecto e salvar esse numero dessa review em algum lugar Y,
# # alem tb de slavar o sentimento dessa reviews em Y
#calcular o score a partir das informaçõe armazenadas em Y



import xml.etree.ElementTree as ET
import collections
from itertools import chain
import os 

'''def BNC_noun_parser(xml_name, desired_tag, searched_token, first_attribute, second_attribute, file_destiny):
                                                                #desired_tag: sentence 
                                                              
                                                              #searched_token deve ser : sentiment
                                                              #first_attribute deve ser passado como: Verypositive
                                                              #second_attribute deve ser: id
                                                              
    
    
    tree = ET.parse(xml_name)
    root = tree.getroot()

    tag_parameter = ".//" + desired_tag
    element = root.findall(tag_parameter)# finds only elements with the tag "w" which are direct children of the current root

    parsed_tokens=[]#list that is going to contain all the nouns extracted form the BNC file

    #if the pos-tagging is a noun(pos="SUBST"), it is stored in the nouns_tokens list
    #the type of tagging for nouns are available in this link: http://www.natcorp.ox.ac.uk/docs/gramtag.html
    
    for desired_tag in element:
        if desired_tag.attrib[searched_token] == first_attribute: 
            parsed_tokens.append(desired_tag.attrib[second_attribute].lower())#the desired noun is an attribute of 'hw'
            #print("tipo: ",type(desired_tag.attrib[second_attribute]))

    with open(file_destiny, 'a+', encoding="utf-8") as f:
        print(' '.join(parsed_tokens), file=f)

BNC_noun_parser("2482.xml", "sentence", "sentiment", "Verypositive", "id", "score2.txt")
#                             desired_tag  searched_token 
'''
#aspects deve ser uma lista com os aspectos a serem buscados 
def BNC_noun_parser(xml_name, sentence, sentiment, VeryPositive, id, file_destiny, aspects):#desired_tag deve ser passada como: "w"
                                                              #VeryPositive deve ser passado como: "SUBST"
                                                              #"sentiment" deve ser : 'pos'
                                                              #second_attribute deve ser: 'hw
                                                              #noun_frequencies é um Counter
    
    
    tree = ET.parse(xml_name)
    root = tree.getroot()

    tag_parameter = ".//" + sentence
    element = root.findall(tag_parameter)# finds only elements with the tag "w" which are direct children of the current root

    parsed_reviews=[]#list that is going to contain all the nouns extracted form the BNC file

    #if the pos-tagging is a noun(pos="SUBST"), it is stored in the nouns_tokens list
    #the type of tagging for nouns are available in this link: http://www.natcorp.ox.ac.uk/docs/gramtag.html
    #desired_sentiments = ["Verypositive", "Positive"]


    desired_nouns=[]
    #desired_POS=["NN", "NNS", "NNP", "NNPS"]
    contador_geral = 0
    lista_id=[]

    for sentence in element:
        sentence.
        aspect_review_counter = 0
        #if sentence.attrib[sentiment] in desired_sentiments: 
            #print("sentence.attrib [id] :",sentence.attrib[id])
            #print("sentence.attrib[sentiment]: ",sentence.attrib["sentiment"])
            #print("sentimentValue: ", sentence.attrib["sentimentValue"])
            #parsed_tokens.append(sentence.attrib[id])#the desired noun is an attribute of 'hw'
            #parsed_tokens.append(sentence.attrib["sentiment"])
            #print("tipo: ",type(sentence.attrib[id]))

        sentence.findall(".//token")
        for tokens in sentence:
            #print("tokens: ",tokens)#a é tokens
            for token in tokens:
                #print("token: ", token)#b é token
                for token_child in token: #coisa eh token_child
                    #print("token_chilçd: ", token_child)
                    '''if coisa.tag == "word":
                        print("coisaword.text: ",coisa.text)'''
                    if token_child.tag =="POS": #and token_child.text in desired_POS: #coisa é POS
                        #print("coisapos.text", coisa.text)
                        #desired_tokens.append(token)
                        for sentence_tags in token:#z são as tags de token: word, lemma, char, etc

                            if sentence_tags.tag == "word":
                                if sentence_tags.text.lower() == aspect:
                                    aspect_review_counter += 1
                                    lista_id.append(sentence.attrib[id])
                                    contador_geral += 1
                                    #print("sentence.attrib [id] :",sentence.attrib[id])
                                    #print("sentence.attrib[sentiment]: ",sentence.attrib["sentiment"])
                                    #print("sentimentValue: ", sentence.attrib["sentimentValue"])
                                    #print("review_counter: ", aspect_review_counter)
                                    #aspect_review_counter += 1
                                    parsed_reviews.append(sentence_tags.text)
    '''    
        N = sentence.attrib[id]
        with open(file_destiny, 'a+', encoding="utf-8") as f:
            print("z.text: ", z.text, file=f)
            print("last id: ", N, file=f)
            print("sentence.attrib [id] :",sentence.attrib[id], file=f)
            print("sentence.attrib[sentiment]: ",sentence.attrib["sentiment"], file=f)
            print("sentimentValue: ", sentence.attrib["sentimentValue"], file=f)
            print("aspect_review_counter: ", aspect_review_counter, file=f)
'''
    with open(file_destiny, 'a+', encoding="utf-8") as f:
        print(' '.join(parsed_reviews), file=f)
        print("parsed tokens size: ",len(parsed_reviews), file=f)

    
    
    #print("Contador geral: ", contador_geral)#esse print testa se encontrou todas as ocorrencias em reviews positivas e mto positivas

    

BNC_noun_parser("2482.xml", "sentence", "sentiment", "Verypositive", "id", "score_test_boy.txt","boy")