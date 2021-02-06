import nltk
import xmltodict
from wrapperWSD import WrapperWSD
import Review
import FilteredSentence

def disambiguate_raw_reviews(all_reviews, babelfy_API_key):
    '''
    This function disambiguates each word in a review.
    For each word, its string receive a babelsynset
    representation.

    Parameters:

        all_reviews: (list): contains all reviews objects of a movie.
        
        babelfy_API_key (string)

    Returns:

        None
    '''
    
    wsd = WrapperWSD()
    print("if you receive 'zero division', 'Keyerror[0]' error or 'empty vocabulary', it's because your babelsynset_key has expired")

    for review in all_reviews:
        #print("raw review :", review.raw_review)
        
        # disambigauted_words is list containing tuples, 
        # in whis information about the word is stored - such
        # as its babelsysnet representation.
        disambiguated_words = wsd.wsdBabelfy(review.raw_review, babelfy_API_key)
        
        #print(disambiguated_words)
        
        for token in disambiguated_words:

            word = token[0]
            babelsynset = token[1]

            word_and_babelsynset = (word, babelsynset)
            #print(word_and_babelsynset)

            # the tuple word_and_babelsynset is appended 
            # to the review object which they belong:
            review.add_noun_and_babelsynset(word_and_babelsynset)
        



def disambiguate_filtered_sentence(all_sentences, babelfy_API_key):
    
    '''
    This function disambiguates each word in a review.
    For each word, its string receive a babelsynset
    representation.

    Parameters:

        all_sentences (list): contains all filtered sentences of a movie
        
        babelfy_API_key (string)

    Returns:

        None
    '''
    
    wsd = WrapperWSD()
    print("if you receive 'zero division', 'Keyerror 0' or 'empty vocabulary' error, it's because your babelsynset_key has expired")
    for filtered_sentence in all_sentences:
        
        if babelfy_API_key == "None":
            disambiguated_words = wsd.wsdBabelfy(filtered_sentence.raw_sentence)
            
        else:
            disambiguated_words = wsd.wsdBabelfy(filtered_sentence.raw_sentence, babelfy_API_key)
            
        
        for token in disambiguated_words:

            word = token[0]
            babelsynset = token[1]

            word_and_babelsynset = (word, babelsynset)
            #print(word_and_babelsynset)

            filtered_sentence.add_babelsynsets_words(word_and_babelsynset)
            
            

# function only for testing:
def disambiguator_test():
    
    wsd = WrapperWSD()
    string = "What is interesting about Grey 's picture is the use of understatement to emphasize the complexity of negotiated relationships in the New York world where mob business and city administration intersect ."
    string2 = 'My sister has a dog. She loves him.'
    #result1 = wsd.wsdNLTK(string)
    result2 = wsd.wsdBabelfy(u'My sister has a dog. She loves him.') 

    print(result2)

if __name__ == "__main__":
    
    
    #nltk.download()


    disambiguator_test()
