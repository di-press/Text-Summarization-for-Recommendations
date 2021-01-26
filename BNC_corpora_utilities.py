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

    #alphabet_string = string.ascii_lowercase
    #alphabet_list = list(alphabet_string)

    BNC_frequency_folder = Path.cwd() / "BNC_noun_frequencies"
    BNC_frequency_folder.mkdir()


    #for letter in alphabet_list:

        #temp_path = BNC_frequency_folder
        #letter = letter + ".txt"
        #temp_path /= letter
        #temp_path.touch()
    
    for word in parsed_tokens:
        
        if word.isalnum():

            file_index = word[0] + ".txt"
            filename = Path("BNC_noun_frequencies", file_index) 
            
            with open(filename, 'a+', encoding="utf-8") as f: 

                print(word, parsed_tokens[word], file=f)
    

def frequency_dict_nouns():
    
    parsed_tokens = extract_BNC_nouns()
    create_BNC_frequency_files(parsed_tokens)


# 251679 itens aproximadamente
# 251679 / 1500 = 168
from pathlib import Path
from collections import Counter
import sqlite3
import time

def create_db():
    
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
    



