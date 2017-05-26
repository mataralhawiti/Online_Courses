from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

sw = stopwords.words("english")
stemmer = SnowballStemmer("english")


print sw[0]
print sw[10]
print len(sw)

print stemmer.stem("responsiveness")
print stemmer.stem("unresponsive")