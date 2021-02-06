import Review
import sqlite3
import string
import numpy as np
import time


def create_synsets_db_optimized():
    '''
    Create a local database to store a babelsynset and its 300 dimensions vector.
    This database is construct using NASARI embbedings.
    The synset is stored as text, and the dimensions too.
    '''
    
    connection = sqlite3.connect("nouns_synsets_optimized.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS nouns_synsets_optimized (
                noun text PRIMARY KEY,
                vector_dimensions text
                )""")

        
    
    with open("babelsynsets_4471657.txt", 'r', encoding="utf-8") as f: 
        
        for line_content in f:
            
            if line_content != "" and line_content != " ":                
                
                babelsynset = line_content.split(" ")[0]
                dimensions = line_content.split(" ")[1:]
                dimensions = " ".join(dimensions)                
                # dimensions is a string holding each vector dimension value,
                # separated by space, like this: "300 398 482 ..."
                cursor.execute("INSERT INTO nouns_synsets_optimized VALUES (?, ?)",
                (babelsynset, dimensions))
                        
    print("creating indexes for db...")
    cursor.execute("CREATE INDEX index_nouns ON nouns_synsets_optimized (noun);")                      
    print("COMMITING INSERTIONS INTO DATABASE...")
    connection.commit()
    cursor.close()
    connection.close()




def search_in_synsets_db_optimized(babelsynsets):

    connection = sqlite3.connect("nouns_synsets_optimized.db")
    cursor = connection.cursor()
    babelsynsets_dimensions = []

    for synset in babelsynsets:

        if synset[:3] != 'bn:':
            synset = "bn:" + synset 
        
        cursor.execute("SELECT * FROM nouns_synsets_optimized WHERE noun=?", (synset,))
        fetched = cursor.fetchall()

        if fetched:      

            found_synset = fetched[0][1]
            #print("found synset :", synset)
            embbeding_values = found_synset.split(" ")
            embbeding_values = list(map(float, embbeding_values))
            embbeding_values_array = np.array(embbeding_values)

            babelsynsets_dimensions.append(embbeding_values_array)
        
        else:
            print("babelsynset not found: ", synset)


    return babelsynsets_dimensions

            



if __name__ == "__main__":
   
    #create_synsets_db_optimized()
    
    lista = ["00090504v", "00028604n", "00116053r", "00071838n"]

    start = time.perf_counter()
    found = search_in_synsets_db_optimized(lista)

    if found:
        print("end of faster process")

        

    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes for faster query: ", elapsed_minutes)


    start = time.perf_counter()
    found = search_in_synsets_db(lista)

    if found:
        print("end of slower process")

        

    end = time.perf_counter()
    # elapsed time is in seconds:
    elapsed_time = end - start
    elapsed_minutes = elapsed_time / 60

    print("elapsed minutes for slower query: ", elapsed_minutes)
    