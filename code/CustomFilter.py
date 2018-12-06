from whoosh.lang.wordnet import Thesaurus
from whoosh.analysis import Filter

from nltk.corpus import wordnet as wn

wordnet_perl_file = '../data/prolog/wn_s.pl'

# f = open(wordnet_perl_file)
# t = Thesaurus.from_file(f)
# f.close()

def return_synonyms(term):
    # syns = t.synonyms(term)
    if len(wn.synsets(term)) == 0:
        return []
    temp = [str(lemma.name()) for lemma in wn.synsets(term)[0].lemmas()]
    syns = []
    for t in temp:
        if t != term and t.isalpha():
            syns.append(t)
    return syns

class CustomFilter(Filter):

    def __call__(self, tokens):
        for t in tokens:
            syns = return_synonyms(t.text)
            syns.append(t.text)
            for syn in syns:
                t.text = syn
                yield t