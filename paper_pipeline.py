#it takes around 45 minutes to execute!
import BNC_nouns_extractor
import reviews_noun_extractor
import counter_occurrences
import KL_divergence
import movie_extractor

def main():

    file_destiny = "corpora_BNC.txt"
    root_directory = "C:\\Users\\User\\Desktop\\ic\\ota_20.500.12024_2554\\2554\\Texts"

    BNC_nouns_extractor.BNC_nouns_extractor(root_directory, file_destiny)

    dirtest = "C:\\Users\\User\\Desktop\\ic\\Reviews\\HetRec_CoreNLP" 
    destiny_file = "corpora_reviews.txt"
    
    reviews_noun_extractor.reviews_noun_extractor(dirtest, destiny_file)

    KL_values = KL_divergence.KL_nouns_values("KL_nouns.txt")

    aspects_dict = KL_divergence.epsilon_aspects_extraction(KL_values, 2000, "aspects_pipeline.txt")

    set_of_movies = []

    directory_path = "C:\\Users\\User\\Desktop\\ic\\xml_reviews"

    movie_extractor.movie_extractor(directory_path, aspects_dict, set_of_movies)



if __name__ == '__main__':
    main()