# Text-Summarization-for-Recommendations 
In construction

## Dependencies
Python = 3.7

## Obtaining BNC (British National Corpus)
Acess the link: https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2554

Click in "Download all local files for this item (538.35MB)", read the Large
size requirement, and click "continue" if you want to download it

After downloading, decompress the folder, and save it inside the directory
of this project. 

Run BNC_frequency_nouns.py and a folder containing txt filetype is going to be 
created, storing all nouns found in BNC. The name of each txt filetype indicates the initial letter of all nouns present in it, and each file contains 
one noun per line, in lowercase - since BNC store them in lowercase, followed by its frequency. As an example, the initial letter of the noun "area" is "a",
and in "a.txt" you are going to find:

area 5804

The final generated folder is around 2,8 MB