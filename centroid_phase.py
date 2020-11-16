# fazer a função que faz a query do babelnet

import numpy as np


"""
    "babelsynsets_4471657.txt" is a file in which each line is a babelsynset
    followed by its 300 dimensions vector values, separated by space.
    This function searchs the babelsynset in the "babelsynsets_4471657.txt"
    file and retrieve its 300 dimensions values.

    If the babelsynset is founded, this function returns its 300 dimensions
    values in form of numpy array. 
    If it is not found, this function returns False
"""

def retrieve_babelsynset_dimensions(desired_babelsynset):

    with open("babelsynsets_4471657.txt", "r", encoding="utf-8") as synsets_file:

        for line in synsets_file:
            # each babelsynset has 12 characters:
            current_synset = str(line[0:12])

            if current_synset == desired_babelsynset:
                # the first element of the list is going to be the
                # desired babelsynset; so, the first element is excluded 
                # from the list, since only the 300 values are needed
                # in the centroid phase:

                desired_babelsynset_dimensions = line.partition(" ")[2]
                
                # split each dimension value in the line by space:
                desired_babelsynset_dimensions = desired_babelsynset_dimensions.split(" ")

                # the values are read as strings. The valuer are converted to float
                # values, and the "\n" character is removed:
                desired_babelsynset_dimensions = list(map(float, desired_babelsynset_dimensions))

                # converting the dimensions into numpy array:
                babelsynsets_dimensions_array = np.array(desired_babelsynset_dimensions)
                
                return babelsynsets_dimensions_array

    return False

'''
    selected_centroid_synsets is a list containing the babelsynset ID
    of the words that were previously selected through the tf-idf algorithm
    to be part of the centroid embbeding.

    This function sum the vectors of the babelsynset nasri embbedings
    (each dimension of a vector is added to the corresponding dimension
    of the other vector, and so on, as in formula 3 of the paper)
'''

def centroid_construction(selected_centroid_synsets):

    # founded_synsets is going to accuse if no synset was found
    # in Nasari embbedings file:
    founded_synsets = False

    centroid_embbeding = np.zeros(300, float)

    for current_babelsynset in selected_centroid_synsets:
        
        current_babelsynset_dimensions = retrieve_babelsynset_dimensions(current_babelsynset)

        # if it is not a boolean variable, the babelsynset was found:
        if type(current_babelsynset_dimensions) != bool:

            # a synset was found:
            founded_synsets = True

            # sum of each dimension 
            centroid_embbeding = centroid_embbeding + current_babelsynset_dimensions

    if founded_synsets == True:
        
        return centroid_embbeding
    else:
        
        return False


def sentence_embbeding_construction():
    

if __name__ == '__main__':

    dimensions = retrieve_babelsynset_dimensions("bn:00000055n")

    if type(dimensions) != bool:
        print(dimensions)
    else:
        print("Not found")
    

    dimensions = retrieve_babelsynset_dimensions("bn:11100055n")

    if type(dimensions) != bool:
        print(dimensions)
    else:
        print("Not found")





