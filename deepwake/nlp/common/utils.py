import os

from six import iteritems


def reverse_dict(d):
    return {v: k for (k, v) in iteritems(dict(d))}

def get_absolute_path(path_name):
    """ get absolute path name.

    Parameters
    ----------
    path_name

    Returns
    -------

    """
    return os.path.join(os.path.split(os.path.realpath(__file__))[0], path_name)


def read_bulks(path):
    bulks = []
    with open(path, mode='r', encoding='UTF8') as reader:
        bulk = []
        for line in reader:
            if line.strip() == '' and bulk:
                bulks.append(bulk)
                bulk = []
            else:
                bulk.append(line)

    return bulks

def read_lines(path):
    with open(path, mode='r', encoding='UTF8') as reader:
        lines = [line for line in reader if line.strip() != '']
    return lines

def load_corpus(corpus_path_dict):
    """

    Parameters
    ----------
    corpus_path_dict

    Returns
    -------

    """
    corpus = {}
    domain_index_dict = {}
    index = 0
    for domain, path in corpus_path_dict.items():
        _path = get_absolute_path(path)
        records = read_lines(_path)
        corpus[domain]= records
        domain_index_dict[domain] = index
        index += 1
    index_domain_dict = reverse_dict(domain_index_dict)
    return corpus, domain_index_dict, index_domain_dict



