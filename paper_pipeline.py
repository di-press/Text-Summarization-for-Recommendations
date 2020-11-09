import BNC_nouns_extractor
import reviews_noun_extractor
import counter_occurrences
import KL_divergence
import Movie
import movie_extractor 

def main():

    # file destiny is the name of the file where the nouns are going to be written:
    file_destiny = "corpora_BNC.txt"

    # root_directory is the folder downloaded and decompressed from BNC:
    root_directory = "C:\\Users\\User\\Desktop\\ic\\ota_20.500.12024_2554\\2554\\Texts"

    BNC_nouns_extractor.BNC_nouns_extractor(root_directory, file_destiny)

    # dirteste is the decompressed folder of the reviews database:
    dirtest = "C:\\Users\\User\\Desktop\\ic\\Reviews\\HetRec_CoreNLP" 

    # destiny_file is the file where the nouns extracted from the reviews are going to be written:
    destiny_file = "corpora_reviews.txt"
    
    reviews_noun_extractor.reviews_noun_extractor(dirtest, destiny_file)

    # The KL value for each noun is going to be written in the file "KL_nouns.txt":
    KL_values = KL_divergence.KL_nouns_values("KL_nouns.txt")

    #value chosen for the KL divergence threshold (should be established better later):
    KL_threshold = 2000 

    aspects_dict = KL_divergence.epsilon_aspects_extraction(KL_values, KL_threshold, "aspects_pipeline.txt")

    set_of_movies = []
    #a pasta xml_reviews é de teste, reunindo um conjunto pequeno de reviews separadamente 

    # the directory above contains the reviews in xml format after applying
    # the CoreNLP sentiment analysis:
    directory_path = "C:\\Users\\User\\Desktop\\ic\\xml_reviews"

    movie_extractor.movie_extractor(directory_path, aspects_dict, set_of_movies, KL_threshold)


    for movie in set_of_movies:
        movie.sentence_filtering()



if __name__ == '__main__':
    # To do:
    main()