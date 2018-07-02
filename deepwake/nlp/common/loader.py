import yaml

# 载入配置文件.
from deepwake.nlp.common.constant import CONFIG_PATH
from deepwake.nlp.common.utils import get_absolute_path

with open(get_absolute_path(CONFIG_PATH), 'r') as reader:
    CONFIG = yaml.load(reader)

def load_dict(path_dict):
    """ 载入词典特征文件.

    Parameters
    ----------
    path_dict

    Returns
    -------

    """
    idx = 0
    word_label_dict = {}
    dict_feature_index_dict = {}
    for dict_name, dict_path in path_dict.items():
        dict_feature_index_dict[dict_name] = idx
        with open(dict_path, 'r') as reader:
            for line in reader:
                word = line.strip()
                if word == '':
                    continue
                if word not in word_label_dict:
                    word_label_dict[word] = set()
                word_label_dict[word].add(dict_name)
        idx += 1
    return word_label_dict, dict_feature_index_dict

# 词 -> 词典标签, 词典特征名称 -> 索引.
WORD_LABEL_DICT, DICT_FEATURE_INDEX_DICT = load_dict(CONFIG['dict'])

def load_suffix(path_dict):
    suffix_dict = {}
    suffix_feature_index_dict = {}
    index = 0
    for suffix_name, suffix_path in path_dict.items():
        suffix_dict[suffix_name] = set()
        suffix_feature_index_dict[suffix_name] = index
        with open(suffix_path, 'r') as reader:
            for line in reader:
                word = line.strip()
                if word == '':
                    continue
                suffix_dict[suffix_name].add(word)
        index += 1
    return suffix_dict, suffix_feature_index_dict

# 载入前后缀词典.
# SUFFIX_DICT, SUFFIX_FEATURE_INDEX_DICT = load_dict(CONFIG['suffix'])


if __name__ == '__main__':
    print(WORD_LABEL_DICT)
    print(DICT_FEATURE_INDEX_DICT)