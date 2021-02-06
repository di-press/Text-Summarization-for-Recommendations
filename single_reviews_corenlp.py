import os
from pycorenlp import StanfordCoreNLP
import string
import time
from pathlib import Path
import string

def parsing_reviews_corenlp():
    '''
    This module do the POS Tagging and sentimental analysis
    through CoreNLP processing. Each single review,
    isolatedly, is parsed, and stored in the "Separated Reviews" 
    folder. 
    
    Before using it, see README for how to connecto to
    CoreNLP server    
    '''

    start = time.perf_counter()
        
    #check in your terminal if the port is adequated. See README for more information.
    nlp = StanfordCoreNLP('http://localhost:9000')

    desired_path = Path.cwd()
    desired_path = Path(desired_path, "Separated Reviews")
    desired_path = desired_path.absolute()

    destiny_folder = Path.cwd()
    destiny_folder = Path(destiny_folder, "single_reviews_corenlp")

    if not destiny_folder.is_dir():
        destiny_folder.mkdir()

    for file in desired_path.iterdir():

        review_text = ""
        with open(file, encoding='utf8') as f: 
            line = f.readlines() 
            review_text += "".join(line)

        review_text = review_text.replace("%", "percent")
        
        if review_text == "":
            continue

        server_answer = nlp.annotate(review_text,
                    properties={
                        'annotators': 'sentiment',
                        'outputFormat': 'xml',
                        'timeout': 50000, 
                    })

        filename = file.name.split(".")
        filename = filename[0] + ".xml"
        directory_name = file.name.split("_")
        directory_name = directory_name[0]


        directory = Path(destiny_folder, directory_name)
    
        if not directory.is_dir():
            directory.mkdir()

        destiny_file = Path(directory, filename)

        error_string = "Could not handle incoming annotation"
        timeout_string = "CoreNLP request timed out. Your document may be too long."

        if server_answer == error_string or server_answer == timeout_string:
            print("error in file: ", filename)

        else:

            with open(destiny_file, 'a+', encoding="utf-8") as f: 

                print(server_answer, file=f)


    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes: ", elapsed_minutes)

