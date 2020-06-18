#eu segui este tutorial: https://towardsdatascience.com/natural-language-processing-using-stanfords-corenlp-d9e64c1e1024

#você pode baixar a Stanford Core NLP manualmente no site oficial, ou então baixar pelo terminal, como consta no tutorial.
#no terminal, entre no diretório em que você baixou a Core NLP e insira o comando:

# java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 50000

# neste comando, '6g' equivale a 6 Gb; no meu pc, decidi colocar no máximo 3Gb. Quanto mais Gb's, mais rápido.
# também é possível inserir Mb: como '20m', por exemplo.
# eu entendi que timeout seria o tempo de espera de uma resposta do servidor, em milisegundos. Optei por usar 50000.
# processamentos de muitos arquivos exigem timeout mais alto, se você for fazer um processamento simples - como
#um teste, por exemplo - pode deixar o timeout em 1000
#textos grandes e/ou com muitas sentenças demoram mais tempo a serem processados

#durante o processamento, fique atento ao terminal, pois lá você terá informações sobre o que está sendo processado
# e se houve algum erro

import os
from pycorenlp import StanfordCoreNLP
import string

nlp = StanfordCoreNLP('http://localhost:9000')


#abaixo, coloque o diretório do seu dataset de reviews. No meu caso, usei os arquivos texto do dataset do Rafael. Estes arquivos
# estão na pasta "separated reviews" da base de dados dele.
directory_path = "C:\\Users\\User\\Desktop\\ic\\Reviews\\reviews HetRec\\Hetrec_reviews\\Separated Reviews\\Separated Reviews"


for file in os.listdir(directory_path):

    current_file = os.path.join(directory_path, file)

    review_text = ""
    with open(current_file, encoding='utf8') as f: 
        result = f.readlines() 
        review_text += "".join(result)

    #"conversão" do arquivo em formato texto para xml (este passo é melhor compreendido na linha 50)
    file_name = file[0 : -3] + "xml"

    #result será o resultado do processamento feito pela CoreNLP
    result = nlp.annotate(review_text,  #review_text (string) é o conteúdo da review a ser processada pela CoreNLP. 
                    properties={
                        'annotators': 'sentiment', #você pode mudar os annotators para pos-tagging, ner, ou outros. Exemplo: 
                        #'annotators': 'sentiment, ner, pos',
                        'outputFormat': 'xml', #output será o tipo de 'formatação' que você deseja a resposta: pode ser xml, json, txt,
                        'timeout': 50000, #coloque o timeout que você digitou no terminal (50000, no meu caso)
                    })

    #apesar do annotator ser só "sentiment", automaticamente o servidor passa o parâmetro 'pos', já que 
    # a análise de sentimentos necessita do pos-tagging - por isso vai demorar bastante

    #abaixo, 'result' deve ser 'impresso' em algum tipo de arquivo. Optei em gerar arquivos do tipo xml, mas você
    #pode escolher o formato que deseja, basta alterar a linha 40 - trocar "xml" por "txt", por exemplo
    #abaixo, cada review processada pela CoreNLP irá gerar um arquivo xml.

    with open(file_name, 'w', encoding="utf-8") as f:
        print(result, file=f)
        