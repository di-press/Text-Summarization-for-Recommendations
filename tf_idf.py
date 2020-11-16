
# need to be commented!
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
        value = number_total_documents/value
        value = math.log2(value)
        total_document_occurences[i] = value
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
    selected to be part of the centroid
'''

def tf_idf_centroid_selection(review, threshold):

    text_data = np.array(review)

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

    number_total_documents = len(auxiliar_dataframe.columns)

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

    selected_centroid_words = {}
    
    for word in dictionary:      
        word_documents_value = dictionary[word]

        for documents in word_documents_value:

            tf_idf_value = word_documents_value[documents]

            if(tf_idf_value > threshold):

                selected_centroid_words[word] = 1

    selected_centroid_words = list(selected_centroid_words)
    
    return selected_centroid_words


if __name__ == "__main__":


    list1 = ['To do is to be. to be is to do',
                        'To be or not to be. Ai am what Ai am',
                        'Ai think therefore Ai am do be do be do',
                        'do do do da da da let it be let it be']


    tf_idf_centroid_selection(list1, 0)
                




