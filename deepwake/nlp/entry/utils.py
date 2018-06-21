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
    for name, file in CONFIG['dict'].items():
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
    pass

