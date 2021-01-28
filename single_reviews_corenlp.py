import os
from pycorenlp import StanfordCoreNLP
import string
import time
from pathlib import Path
import string

'''
    This module do the POS Tagging and sentimental analysis
    through CoreNLP processing. Each single review,
    isolatedly, are parsed, and stored in the "Separated Reviews" 
    folder. Finally, this folder is going to have another folder 
    representing the movie name, and inside each folder, there 
    will be xml files representing each review of the movie.
    
'''

start = time.perf_counter()
    

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

    # CoreNLP parser doesn't recognize the % char:
    review_text = review_text.replace("%", "percent")
    
    # avoid that an empty string is parsed:
    if review_text == "":
        continue

    server_answer = nlp.annotate(review_text,
                properties={
                    'annotators': 'sentiment',
                    'outputFormat': 'xml',
                    'timeout': 70000, 
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

    # if the server returns an error message, nothing needs to be generated
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

