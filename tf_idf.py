
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import math 
from collections import OrderedDict

# treat the case which has only one document, if it exists

'''
    when this function is applied, the dataframe already contains
    the frequency of each word, per cell.
    
    tf = 1 + log2(f_i,j)
    f_i,j = frequency of the term i in document j

'''
def tf(cell_value):

    if cell_value != 0:
        cell_value = (math.log2(cell_value)) + 1
        return cell_value
    return 0

def idf(dataframe):

    total_document_occurences = []

    for row in range(len(dataframe)):

        array_row_values = np.array(dataframe.iloc[row])
        #print(array_row_values)
        number_document_occurrences = 0
        
        for document_index in array_row_values:
            
            if document_index > 0:
                number_document_occurrences = number_document_occurrences + 1
        
        total_document_occurences.append(number_document_occurrences)

    number_total_documents = len(dataframe.columns)

    i = 0

    for value in total_document_occurences:
        
        idf_value = number_total_documents/value
        idf_value = math.log2(idf_value)
        total_document_occurences[i] = idf_value
        i = i + 1 
    
    dataframe['idf'] = total_document_occurences 

    return dataframe

'''
    tf_idf(dataframe):

    This function only should be applied to the dataframe after 
    the tf and idf function were already applied
'''     

def tf_idf(dataframe):

    idf_values = np.array(dataframe['idf'])

    for column_index in range(len(dataframe.columns)-1):
        
        current_column = np.array(dataframe.iloc[:, column_index])
        document_tf_idf_values = np.multiply(current_column, idf_values)

        #normalizing each document:
        current_document_norm = np.linalg.norm(document_tf_idf_values, 2) 
        normalized_tf_idf_values = np.divide(document_tf_idf_values, current_document_norm)

        column_name = "tf_idf_document" + str(column_index)
        dataframe[column_name] = normalized_tf_idf_values 
    
    return dataframe

'''
    this function returns the words in the reviews that were 
    selected to be part of the centroid. Each review
    is considered as a document to tf-idf algorithm
'''

def tf_idf_centroid_selection(movie_reviews, threshold):

    text_data = np.array(movie_reviews)

    # create the bag of words feature matrix
    count = CountVectorizer()
    bag_of_words = count.fit_transform(text_data)

    # get feature names
    feature_names = count.get_feature_names()


    auxiliar_dataframe = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)
    # now the auxiliar dataframe has a word representing each row, 
    # and the columns represents a document. In each cell, we have the frequency
    # of the word in the respective document.

    auxiliar_dataframe = auxiliar_dataframe.transpose()
    auxiliar_dataframe = auxiliar_dataframe.applymap(tf) 
    #pd.set_option('display.max_rows', None)
    #print("auxiliar dataframe: ", auxiliar_dataframe)

    number_total_documents = len(auxiliar_dataframe.columns)
    #print("number of total documents: ", number_total_documents)

    dataframe_final = idf(auxiliar_dataframe)  

    current_column = np.array(dataframe_final.iloc[:, 0])
    dataframe_tf_idf = tf_idf(dataframe_final)
    # now the auxiliar_dataframe is structured as: 
    #       
    # word1
    # word2
    # ...
    # wordn 
    print(dataframe_tf_idf)

    last_columns_of_values = (-1 * number_total_documents)

    dataframe_only_columns = dataframe_tf_idf[dataframe_tf_idf.columns[last_columns_of_values:]]
    
    dictionary = dataframe_only_columns.to_dict(orient="index")

    selected_centroid_words = []
    
    for word in dictionary:      
       if word != 'bn':
            word_documents_value = dictionary[word]

            for documents in word_documents_value:

                tf_idf_value = word_documents_value[documents]

                if(tf_idf_value > threshold):

                    selected_centroid_words.append(word)
    # set doesn't allow duplicated words:
    selected_centroid_words = set(selected_centroid_words)
    
    return selected_centroid_words


if __name__ == "__main__":

    babelsynsets = ['bn:00085522v bn:00045772n bn:00079017n bn:00082195v bn:00021383n', 
    'bn:00091037v bn:00045161n bn:00041611n bn:03417526n bn:00045018n', 
    'bn:00022991n bn:00055408n bn:00014137n bn:03335997n'] 


    list1 = ["Down to You: Boy meets girl, they fall in love, relationship cools, couple breaks up and each is tortured by thoughts of What if",
                        " I decided to see this movie because I enjoyed Julia Stiles' performance in 10 Things I Hate About You. However, after seeing the marquee poster - a knockoff of The Very Thought of You - I scaled down my expectations and braced for a painful two hours. My prediction was partially correct. Unlike the typical teen oriented romantic comedy there was an attempt to infuse this movie with a bit of reality. Unfortunately, the writers apparently could not decide if they wanted to make a romantic comedy or a serious relationship movie. The result is a confused mess: a ludicrous subplot about a student's burgeoning career as a pornographer gets far more screen time than does the terrified couple trying to come to grips with a potential pregnancy. The second problem is the chemistry between Stiles and Freddie Prinze Jr - there is none (I blame the casting director for this). Although both actors have screen presence, they don't click as a duo, consequently, their interactions- especially the fight scenes -do not ring true. Their job is made doubly difficult by having to utter stupid lines. This movie has been targeted to a certain market, and will probably do well. Too bad." ,
                        "Down to You was slammed by critics when it was released, claiming it to be unoriginal, unfunny and really a waste of time. Pay no attention to them. It is rare for romantic comedies to be entirely original [they are after all dealing with love], but Down to You does have it's moments differing it from most of the recently released teen comedies [to which it has constantly been compared]. Through narration by both protagonists the audience is able to see the development of both characters in the long-term and how they ultimately react to each other. Freddie Prinze Jr and Julia Stiles were perfectly cast and behaved as mature young adults for the majority of the film [sparing the audience from cliched teen talk]. They leave the zaniness to their co-stars, which was a good move. The film is more of a love story then most recent teen flicks dealing mainly with physical attraction or opposites attract. One problem with Down to You however is it's not presented well enough to keep the audience interested. Perhaps in the hands of a more capable director this would be achieved, as I got a bit bored with a few of the scenes and some jokes really fall flat. Because of this, it's not as memorable as other teen flicks such as 10 Things or Scream, even. as it's pacing is quite slow. It's saving grace is the cast. Henry Winkler gives a comic performance as Prinze's celebrity-chef father and Zak Orth plays Prinze's friend turned movie- star-friend with gutso. Selma Blair gave a sultry performance but lacked development making her nothing more than the porn star girl. Compared to the other three major teen romance flicks of the year (Loser, Whatever it Takes, Boys and Girls) Down to You is indeed one of the finest. It just needed more oomph to make it more memorable. 7/10"]


    result = tf_idf_centroid_selection(babelsynsets, 0.2)

    print(result)
                




