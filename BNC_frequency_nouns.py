import xml.etree.ElementTree as ET
import collections
from itertools import chain
import os 
from pathlib import Path
from collections import Counter
import string

def BNC_noun_parser (xml_name, 
                     desired_tag,           
                     searched_token,        
                     first_attribute,       
                     second_attribute,     
                     parsed_tokens):         

    """This function extracts all the present nouns in the current xml file.
       

    Args:
        xml_name (str): The current xml file to be parsed

        desired_tag (str): The tag should be passed as "w", since this is 
        the tag to be found in the BNC xml 
        
        searched_token (str): The token should be passed as "pos", since 
        the token we are looking for in the BNC xml tree is "pos". 

        first_attribute (str): The attribute should be passed as "SUBST", since
        this is the grammatical class we are looking for in the BNC xml tree.
        The type of tagging for nouns are available in this link:
        http://www.natcorp.ox.ac.uk/docs/gramtag.html

        second_attribute (str): This attribute should be passed as "hw"

        parsed_tokens(list): list that is going to contain all the nouns extracted from 
        the BNC file; if the pos-tagging is a noun(pos="SUBST"), it is stored in the 
        parsed_tokens list.

    Returns:
        None
    """                                                             
                                                                                                                                   
    tree = ET.parse(xml_name)
    root = tree.getroot()

    tag_parameter = ".//" + desired_tag

    # finds only elements with the tag "w" which
    #are direct children of the current root:
    element = root.findall(tag_parameter)
       
    
    for desired_tag in element:
        #current_attribute represents the grammatical class of the word traversed in the BNC xml tree
        current_attribute = desired_tag.attrib[searched_token]

        #if the grammatical class represents a noun, then the noun should be appended to the list
        if current_attribute == first_attribute: 
            
            #the desired nouns are attributes of 'hw'
            found_noun = desired_tag.attrib[second_attribute] 

            # some nouns in BNC were "glued" like: "banana/orange",
            # so they are splitted in two nouns in this example
            found_noun = found_noun.split("/")

            for splitted_noun in found_noun:

                parsed_tokens.append(splitted_noun)


def extract_BNC_nouns():
    '''
        Function that iterates through all xml files
        in BNC, and all the extracted nouns and its frequencies
        are stored in a Counter object (parsed_tokens).

        Before executign this function, check if your downloaded 
        BNC folder is in the format above:
        this_current_directory -> ota_20.500.12024_2554 -> 2554 -> download -> Texts

        Returns:
        parsed_tokens (Counter) : store each noun and its occurrence number
        in BNC

    '''
    #current path:
    desired_path = Path.cwd()
    # check if your downloaded BNC folder is in the format above:
    desired_path = Path(desired_path, "ota_20.500.12024_2554", "2554", "download", "Texts")
    desired_path = desired_path.absolute()
    

    parsed_tokens = []

    for directory in desired_path.iterdir():

        for subdirectory in directory.iterdir():

            for file in subdirectory.iterdir():

                BNC_noun_parser(file, "w", "pos", "SUBST", "hw", parsed_tokens)


    parsed_tokens = Counter(parsed_tokens)

    return parsed_tokens


def create_BNC_frequency_files(parsed_tokens):

    '''
        Function to create a subfolder and populate with ".txt" files,
        containing the nouns and its frequency.
        As an example, the file "a.txt" contains all extracted nouns with the initial
        letters "a", one word per line, followed by its frequency:

        area 58048
    '''


    BNC_frequency_folder = Path.cwd() / "BNC_noun_frequencies"
    # create a new subfolder called "BNC_noun_frequencies"
    BNC_frequency_folder.mkdir()

    
    for word in parsed_tokens:
        
        # check if the noun stored in BNC is valid
        # (is not a number, is not a symbol, etc)
        if word.isalnum():

            # creates a filename with the initial letter of the noun:
            file_index = word[0] + ".txt"
            filename = Path("BNC_noun_frequencies", file_index) 
            
            # if the file didn't exist, it is created; otherwise, it is just opened:
            with open(filename, 'a+', encoding="utf-8") as f: 

                print(word, parsed_tokens[word], file=f)
    

def frequency_dict_nouns():
    '''
        Function responsible for executing all the process
        of parsing the nouns in BNC and generating a new directory,
        in which each noun and its frequency are stored for further
        processings.
    '''
    
    parsed_tokens = extract_BNC_nouns()
    create_BNC_frequency_files(parsed_tokens)



'''
The function above probably won't be used anymore

def BNC_nouns_extractor(root_directory, file_destiny):

    """Trasverse the folder "Texts" contained in the BNC database. The folder
    "Texts" contains the xml files of the database, which nouns are going
    to be extracted and written in "corpora_BNC.txt", if printing is desired

    Args:
        root_directory (str): The directory on your computer for the folder
        "Texts" that was downloaded from BNC database

        file_destiny (str): the file that are going to contain all the nouns extracted
        from the BNC. If printing is not desired, this parameter should be passed
        as "none"

    Returns:
        parsed_tokens (list) : list containing all the nouns extracted from the BNC
    
    """    
    #the below line clears the file:
    open(file_destiny, 'w').close() 

    parsed_tokens = []

    for subdir, dirs, files in os.walk(root_directory):
        for file in files:                      
            xml_file = os.path.join(subdir, file)
            BNC_noun_parser(xml_file, "w", "pos", "SUBST", "hw", parsed_tokens)

    if file_destiny != "none":

        #print the found nouns in the ".txt" file:
        with open(file_destiny, 'a+', encoding="utf-8") as destiny:
            print(' '.join(parsed_tokens), file=destiny)


    return (parsed_tokens)

'''

#test:
if __name__ == '__main__':

    frequency_dict_nouns()



