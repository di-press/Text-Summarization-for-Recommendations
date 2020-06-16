import os
from pycorenlp import StanfordCoreNLP
import string

nlp = StanfordCoreNLP('http://localhost:9000')


#directory_path = "C:\\Users\\User\\Desktop\\ic\\Reviews\\reviews HetRec\\Hetrec_reviews\\Separated Reviews\\corenlpteste"
directory_path = "C:\\Users\\User\\Desktop\\ic\\Reviews\\reviews HetRec\\Hetrec_reviews\\Separated Reviews\\Separated Reviews"


for file in os.listdir(directory_path):

    current_file = os.path.join(directory_path, file)

    review_text = ""
    with open(current_file, encoding='utf8') as f: 
        res = f.readlines() 
        review_text += "".join(res)


    file_name = "x" + file[0 : -3] + "xml"


    res = nlp.annotate(review_text,
                    properties={
                        'annotators': 'sentiment',
                        'outputFormat': 'xml',
                        'timeout': 50000,
                    })


    with open(file_name, 'w', encoding="utf-8") as f:
        print(res, file=f)
        