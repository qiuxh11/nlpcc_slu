from itertools import chain
from deepwake.nlp.common.utils import read_bulks
from deepwake.nlp.corpus.query_parser import NLPCCQueryParser
from deepwake.nlp.corpus.session import Session


class Corpus:

    def __init__(self, path, parser=None):
        self.path = path
        self.parser = parser
        self.sessions = []

    def set_parser(self, parser):
        self.parser = parser

    def get_sessions(self):
        bulks = read_bulks(self.path)
        bulks.remove(bulks[0])

        for bulk in bulks:
            session = Session(bulk)
            session.parse_queries(self.parser)
            self.sessions.append(session)

        return self.sessions

    def get_corpus_of_domain(self, domain=None, intent=None):
        if domain is None and intent is None:
            raise ValueError("domain and intent are both None!")

        queries = chain(*[session.queries for session in self.sessions])

        if domain is not None and intent is None:
            res = [query for query in queries if query.domain == domain]
        elif domain is None and intent is not None:
            res = [query for query in queries if query.intent == intent]
        else:
            res = [query for query in queries if query.intent == intent and query.domain == domain]
        return res




if __name__ == '__main__':
    corpus = Corpus('../entry/corpus/music')
    parser = NLPCCQueryParser()
    corpus.set_parser(parser)
    sessions = corpus.get_sessions()
    for s in sessions:
        print(s)

    res = corpus.get_corpus_of_domain('music', 'play')
    for r in res:
        print(r)
