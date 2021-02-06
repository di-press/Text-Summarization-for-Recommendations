from py_babelnet.calls import BabelnetAPI
import FilteredSentence
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation

def mapping_words_and_babelsysnets(tf_idf_selected_words, babelfy_API_key):
          
    '''
    Function to map each word with its babelsynset representation
    withou disambiguating. That means that the first selected
    babelsynset retrieved is selected.

    Parameters:
        tf_idf_selected_words (list): contains words selected
            through the tf_idf phase

    Returns:
        synsets_to_search(list): the babelsynsets representing
            the words

    '''
    api = BabelnetAPI(babelfy_API_key)

    for word in tf_idf_selected_words:

        synsets_to_search = []

        senses = api.get_senses(lemma = word, searchLang = "EN")       
        
        if not senses:
            continue

        babelsynset = senses[0]['properties']['synsetID']['id']

        synsets_to_search.append(babelsynset)

    return synsets_to_search

            



def process_filtered_sentences(sentence_candidates, babelfy_API_key):
     
    '''
    Function to process the filtered sentences.
    Stemming is not performed.

    Parameters:
        sentence_candidates: the sentneces selected in sentence 
            filtering phase
        babelfy_API_key (string)

    Returns:
        
        None

    '''

    api = BabelnetAPI(babelfy_API_key)

    for filtered_sentence in sentence_candidates:

        processed_sentence = strip_punctuation(filtered_sentence.raw_sentence)
        processed_sentence = remove_stopwords(processed_sentence)
        list_of_words = processed_sentence.split(" ")

        
        for word in list_of_words:
        
            senses = api.get_senses(lemma = word, searchLang = "EN")       
            
            if not senses:
                continue

            babelsynset = senses[0]['properties']['synsetID']['id']

            word_and_babelsynset = (word, babelsynset)

            filtered_sentence.add_babelsynsets_words(word_and_babelsynset)