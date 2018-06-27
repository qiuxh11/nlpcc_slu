import os

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

