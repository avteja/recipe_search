from whoosh.lang.wordnet import Thesaurus
from whoosh.analysis import Filter

wordnet_perl_file = '../data/prolog/wn_s.pl'

f = open(wordnet_perl_file)
t = Thesaurus.from_file(f)
f.close()

def return_synonyms(term):
    syns = t.synonyms(term)
    return syns

class CustomFilter(Filter):

    def __call__(self, tokens):
        for t in tokens:
            syns = return_synonyms(t.text)
            syns.append(t.text)
            for syn in syns:
                t.text = syn
                yield t