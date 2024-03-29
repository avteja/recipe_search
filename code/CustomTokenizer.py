from whoosh.compat import u, text_type
from whoosh.analysis.acore import Composable, Token

from whoosh.analysis import Tokenizer

from whoosh.lang.wordnet import Thesaurus

from nltk.corpus import wordnet as wn

wordnet_perl_file = '../data/prolog/wn_s.pl'

f = open(wordnet_perl_file)
t = Thesaurus.from_file(f)
f.close()

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

class CustomTokenizer(Tokenizer):

    def __call__(self, value, positions = False, start_pos = 0, **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        token = Token(positions, **kwargs)
        pos = start_pos
        syns = return_synonyms(value)
        syns.append(value)
        for syn in syns:
            token.text = syn
            if positions:
                token.pos = pos
            yield token
