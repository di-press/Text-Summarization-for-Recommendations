#testando a biblioteca kkk

from gensim.parsing.preprocessing import remove_stopwords

string = "Nick likes to play football, however he is not too fond of tennis."

result = remove_stopwords(string)

print(result)