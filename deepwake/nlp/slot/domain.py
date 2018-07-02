import jieba

from deepwake.nlp.common.loader import CONFIG
from deepwake.nlp.common.utils import read_lines
from deepwake.nlp.corpus.corpus import Corpus
from deepwake.nlp.corpus.query_parser import NLPCCQueryParser
from deepwake.nlp.lang.sentence import Sentence
from deepwake.nlp.slot.utils import convert_to_crf_format

NLPCC_QUERY_PARSER = NLPCCQueryParser()

class Domain(object):


    def __init__(self, domain_name=None):
        self.domain_name = domain_name

    def set_domain_name(self, domain_name):
        self.domain_name = domain_name

    def get_data(self, corpus_path, domain_path, error_sentence_path, parser=NLPCC_QUERY_PARSER):
        corpus = Corpus()
        corpus.get_sessions(corpus_path, parser)
        domain_queries = corpus.get_corpus_of_domain(self.domain_name)

        domain_file = open(domain_path, 'w')

        for query in domain_queries:
            sentence = Sentence(query.sentence)
            sentence.cut()
            slot_values = query.slot_values
            temp = convert_to_crf_format(sentence, query.intent, slot_values)
            if temp:
                domain_file.write('\n'.join(temp) + '\n\n')

        domain_file.close()


def set_suggest_by_file(file_path):
    """

    Parameters
    ----------
    file_path : str

    Returns
    -------

    """
    sentences = read_lines(file_path)
    for sentence in sentences:
        splits = sentence.split(' ')
        if len(splits) == 2:
            jieba.suggest_freq((splits[0], splits[1]), True)

if __name__ == '__main__':
    domain = Domain('music')
    domain.get_data(CONFIG['domain']['music'], CONFIG['music_slot_path'], None)





