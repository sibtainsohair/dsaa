from negation_test import AntonymReplacer
import nltk

replacer = AntonymReplacer()
#replacer.replace('good')
#replacer.replace('uglify')
#word_data = "lets not uglify pur code"
#sent = nltk.word_tokenize(word_data)
sent = ["let's", 'not', 'uglify', 'our', 'code']
result = replacer.replace_negations(sent)
print(result)
