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

inicio = time.perf_counter()

nlp = StanfordCoreNLP('http://localhost:9000')

desired_path = Path.cwd()
desired_path = Path(desired_path, "Separated Reviews")
desired_path = desired_path.absolute()

destiny_folder = Path.cwd()
destiny_folder = Path(destiny_folder, "single_reviews_corenlp")
destiny_folder.mkdir()

for file in desired_path.iterdir():

    review_text = ""
    with open(file, encoding='utf8') as f: 
        line = f.readlines() 
        review_text += "".join(line)

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
    print(filename)
    print(directory_name)


    directory = Path(destiny_folder, directory_name)
 
    if not directory.is_dir():
        directory.mkdir()

    destiny_file = Path(directory, filename)

    with open(destiny_file, 'a+', encoding="utf-8") as f: 

        print(server_answer, file=f)

