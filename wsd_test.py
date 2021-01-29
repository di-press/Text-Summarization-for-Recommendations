import nltk
import xmltodict
from wrapperWSD import WrapperWSD


wsd = WrapperWSD()
result = wsd.wsdBabelfy(u'My sister has a dog. She loves him.')
print(f"result: {result}")


