import xml.etree.ElementTree as ET
import collections
from itertools import chain
import os 
from pathlib import Path
from collections import Counter
import string
import sqlite3
import time

def BNC_noun_parser (xml_name, 
                     desired_tag,           
                     searched_token,        
                     first_attribute,       
                     second_attribute,     
                     parsed_tokens):         

    """This function extracts all the present nouns in the BNC xml files.
        It is used only to create BNC_nouns.db, by writing in a file
        each noun per line, followeb by its occurrence.
       

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
    Function to trasverse all the BNC xml files. Only used if you need to generate
    BNC_nouns.db

    Return:
    parsed_tokens (Counter): map a given noun and its BNC number of occurrences
    '''
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
    Function only needed if generating BNC_nouns.db is desired.
    It prints all founded nouns and its frequency in txt files
    '''

    BNC_frequency_folder = Path.cwd() / "BNC_noun_frequencies"
    BNC_frequency_folder.mkdir()


    
    for word in parsed_tokens:
        
        if word.isalnum():

            file_index = word[0] + ".txt"
            filename = Path("BNC_noun_frequencies", file_index) 
            
            with open(filename, 'a+', encoding="utf-8") as f: 

                print(word, parsed_tokens[word], file=f)
    
    
# only used for test:
def frequency_dict_nouns():
    
    parsed_tokens = extract_BNC_nouns()
    create_BNC_frequency_files(parsed_tokens)



def create_db():
    '''
    Inser each noun found in BNC and its occurrence in the BNC_nouns.db
    '''
    
    connection = sqlite3.connect("BNC_nouns.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE nouns_frequencies (
                noun text,
                BNC_frequency integer
                )""")
    
    current_directory = Path.cwd()
        
    parsed_BNC_directory = Path(current_directory, "BNC_noun_frequencies")
            

    for filepath in  parsed_BNC_directory.iterdir():
        print(filepath)
        
        with open(filepath, 'r', encoding="utf-8") as f: 
            
            for line_content in f:
                
                line_content = line_content[:-1]
                
                if line_content != "" and " ":                
                    line_content = line_content.split(" ")
                    

                    if line_content[0] != "":
                        word = line_content[0]

                        if line_content[1]:
                            frequency = line_content[1]
                            frequency = int(frequency)

                   

                            cursor.execute("INSERT INTO nouns_frequencies VALUES (?, ?)",
                            (word, frequency))
                        
                        
    print("COMMITING INSERTIONS INTO DATABASE...")
    connection.commit()
    cursor.close()
    connection.close()



def search_noun_BNC_db(movie_nouns_occurrences):
    '''
    Search noun in BNC_nouns.db and retrieves it values: the noun(text) and its frequency (int).
    Later, maps each noun with its frequency in a movie corpora and in BNC corpora.

    Args:
    movie_nouns_occurrences (dict): dict containing a noun present in a movie corpora and its frequency
    in movie reviews


    Return:

    nouns_corporas_occurrences (tuple): (noun string, frequency of this noun in review corpora, frequency of this noun in BNC)

    '''

    connection = sqlite3.connect("BNC_nouns.db")
    cursor = connection.cursor()

    directory = Path.cwd()
    directory = Path(directory, "BNC_noun_frequencies")
    directory.absolute()

    nouns_corporas_occurrences = []

    for word in movie_nouns_occurrences.keys():

        found = False

        cursor.execute("SELECT * FROM nouns_frequencies WHERE noun=?", (word,))
        fetched = cursor.fetchall()

        if fetched:
            #print(fetched[0][0], fetched[0][1])
            BNC_noun_occurrence = int(fetched[0][1])
            found = True
        
        else:
            BNC_noun_occurrence = 0


        noun_values = (word, movie_nouns_occurrences[word], BNC_noun_occurrence)
        nouns_corporas_occurrences.append(noun_values)


    return nouns_corporas_occurrences

def create_db_test():

    start_creating_db = time.perf_counter()
    create_db()
    end_creating_db = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end_creating_db - start_creating_db
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)
              


#test:
if __name__ == '__main__':

    # frequency_dict_nouns()
    create_db_test()
    



