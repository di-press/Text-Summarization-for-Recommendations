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
                desired_babelsynset_dimensions = line.split(" ")

                # the values are read as strings. Converting them to numbers:
                desired_babelsynset_dimensions = list(map(float, desired_babelsynset_dimensions))


                babelsynsets_dimensions_array = np.array(desired_babelsynset_dimensions)
                
                return babelsynsets_dimensions_array

    return False





