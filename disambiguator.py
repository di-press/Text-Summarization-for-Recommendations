import nltk
import xmltodict
from wrapperWSD import WrapperWSD
import Review
import FilteredSentence

def disambiguate_raw_reviews(all_reviews, babelfy_API_key):
    '''
    all_reviews is a list containing all  reviews of a movie.
    '''
    wsd = WrapperWSD()
    print("if you receive 'zero division' error, it's because your babelsynset_key has expired")

    for review in all_reviews:
        #print("raw review :", review.raw_review)
        if babelfy_API_key == "None":
            disambiguated_words = wsd.wsdBabelfy(review.raw_review)
            #print(disambiguated_words)
        else:
            disambiguated_words = wsd.wsdBabelfy(review.raw_review, babelfy_API_key)
            #print(disambiguated_words)
        
        for token in disambiguated_words:

            word = token[0]
            babelsynset = token[1]

            word_and_babelsynset = (word, babelsynset)
            #print(word_and_babelsynset)

            review.add_noun_and_babelsynset(word_and_babelsynset)
        
            
def disambiguate_filtered_sentence(all_sentences, babelfy_API_key):
    '''
    all_sentences is a list containing all  filtered sentences of a movie
    '''
    wsd = WrapperWSD()
    print("if you receive 'zero division' error, it's because your babelsynset_key has expired")
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
            
            


def disambiguator_test():
    
    wsd = WrapperWSD()
    string = "What is interesting about Grey 's picture is the use of understatement to emphasize the complexity of negotiated relationships in the New York world where mob business and city administration intersect ."
    string2 = 'My sister has a dog. She loves him.'
    #result1 = wsd.wsdNLTK(string)
    result2 = wsd.wsdBabelfy(u'My sister has a dog. She loves him.') #wsd.wsdBabelfy(u"What is interesting about Grey 's picture is the use of understatement to emphasize the complexity of negotiated relationships in the New York world where mob business and city administration intersect .Wahlberg 's comparative lack of expressiveness suits his role as a minor crook out of jail and wanting to go straight ; it 's echoed in his mother 's passivity , and her statement that the two of them have this in common .He 's not stupid , but he 's tentative as he emerges from jail back into the world ; his uncle is willing to help , but has complex and risky operations that make him cautious .In any event , Wahlberg 's tentativeness leads him instead to his old and apparently warm friend , who 's grown into slack opportunism ( as his uncle clearly knows , and would like to keep his nephew away from ) .When the friend stupidly kills the yard manager , he tries to spare his pal , but finally lets the latter take the rap and run off ( in violation of his parole ) .The film gets interesting at this point : one expects Wahlberg to be the victim , but he has figured out that he 's been set up , that even his uncle is willing to have him killed to cover up the crime , and that he 's got to drop his earlier loyalties and figure out a way to clear and protect himself at the same time .The solution is a real New York compromise between truth and justice : the identifying cop is paid off , the real crook kills his true love inadvertently and , crushed with anguish , is taken .Wahlberg has set himself right with the law , probably will be used by one side or the other of the warring tracks manufacturing moguls , crime and bribery continue as always in the Big Apple .What 's refreshing about the picture is its calmness of tone -- the violence is justified but not overdone , the acting has the assurance of real people doing what they must .Poor photography at times -- confusing shots which add to the difficulty of following a complex plot .But it 's a better picture than comments suggest .")
    #result2 = wsd.wsdBabelfy(string2, key='08e51760-1296-41a0-bfb5-8d9545674df8')
    #
    #print(result1)
    print(result2)

if __name__ == "__main__":
    
    
    #nltk.download()


    disambiguator_test()
