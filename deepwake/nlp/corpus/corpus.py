from itertools import chain
from deepwake.nlp.common.utils import read_bulks
from deepwake.nlp.corpus.query_parser import NLPCCQueryParser, QueryParser
from deepwake.nlp.corpus.session import Session


class Corpus:

    def __init__(self):
        self.sessions = []

    def get_sessions(self, paths, parsers):
        if isinstance(paths, str):
            paths = [paths]

        if isinstance(parsers, QueryParser):
            parsers = [parsers]

        for idx, path in enumerate(paths):
            bulks = read_bulks(path)
            # bulks.remove(bulks[0])
            self.parser = parsers[idx]

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

