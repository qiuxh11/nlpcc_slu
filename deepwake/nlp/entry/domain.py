from deepwake.nlp.common.loader import CONFIG
from deepwake.nlp.corpus.corpus import Corpus
from deepwake.nlp.corpus.session import Query
from deepwake.nlp.entry.model import FeatureAddition, Model

feature_addition = FeatureAddition()
feature_addition.config(CONFIG['model']['feature'], CONFIG['model']['processor'])
model = Model()
paths = []
parsers = []

mod = __import__('deepwake.nlp.corpus.query_parser', fromlist=['query_parser'])

for domains in CONFIG['domain']:
    for _, domain in domains.items():
        paths.append(domain['corpus_path'])
        parser_name = getattr(mod, domain['parser'])
        parser = parser_name()
        parsers.append(parser)

# 载入对话语料
corpus = Corpus()
corpus.get_sessions(paths, parsers)

model.set_feature_addition(feature_addition)
model.create_train_data(corpus, CONFIG['model']['train_data'])
model.train_and_test(Query.DOMAIN_DICT)

def get_domain(sentence, response=None, register=None):
    """ 获得对话的域: 火车, 飞机, 酒店, 闲聊等域

    Parameters
    ----------
    sentence: str
        用户对话.

    Returns
    -------
        域的类别:TOPIC_DICT = {
                               0: "traffic",
                               1: "hotel",
                               2: "chat",
                               3: "train",
                               4: "flight"
                            }
    """
    pass


if __name__ == '__main__':
    pass
