import os
import yaml


def get_absolute_path(path_name):
    """ get absolute path name.

    Parameters
    ----------
    path_name

    Returns
    -------

    """
    return os.path.join(os.path.split(os.path.realpath(__file__))[0], path_name)


CONFIG_PATH= './conf/config.yaml'

with open(get_absolute_path(CONFIG_PATH), 'r') as reader:
    CONFIG = yaml.load(reader)

WORD_DICT = {}
DICT_FEATURE_INDEX = {}


def load_dict():
    index = 0
    for name, file in CONFIG['domain_feature_dict'].items():
        path = get_absolute_path(file)
        DICT_FEATURE_INDEX[name] = index
        index += 1
        with open(path, 'r') as reader:
            for line in reader:
                WORD_DICT[line.strip()] = name


# 载入词典
load_dict()


def load_train_corpus(path_dict):
    """ 载入训练语料.

    Returns
    -------
        dict={name0: corpus0,
              name1: corpus1,
              name2: corpus2,
              ...: ...}
    """
    corpus = {}
    for name, path in CONFIG['domain_train_corpus'].items():
        temp = set()
        with open(get_absolute_path(path), 'r') as reader:
            for line in reader:
                temp.add(line.strip())
        corpus[name] = temp
    return corpus


def append_train_corpus(path):
    """ 追加标注的训练语料.

    Parameters
    ----------
    path

    Returns
    -------

    """
    corpus = load_train_corpus()
    # path = get_absolute_path(path)
    with open(path, 'r') as reader:
        for line in reader:
            sample = line.split("@@")
            sample = [sam.strip() for sam in sample]
            if len(sample) == 2 and  corpus.get(sample[1], -1) != -1:
                corpus[sample[1]].add(sample[0])

    for name, path in CONFIG['train_corpus'].items():
        path_name = get_absolute_path(path)
        if os.path.exists(path_name):
            os.remove(path_name)
        with open(path_name, 'a') as appender:
            for sample in corpus[name]:
                appender.write(sample + '\n')












