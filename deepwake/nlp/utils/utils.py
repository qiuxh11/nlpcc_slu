import os
import random
import jieba.posseg as pseg
import jieba

local_dir = os.path.dirname(os.path.realpath(__file__))


def get_traing_dev_set(list, training_rate=0.9):
    """

    Parameters
    ----------
    list : list
    training_rate : float

    Returns
    -------

    """
    random.shuffle(list)
    training_size = (int)(len(list) * (training_rate))
    training_data = list[0:training_size]
    dev_data = list[training_size:]
    print('train size: %d, dev size: %d' % (training_size, len(list) - training_size))
    return training_data, dev_data

def load_sentences_from_file(file_path):
    with open(file_path, 'r', encoding='UTF8') as reader:
        sentences = []
        for line in reader.readlines():
            line = line.strip()
            if line == "":
                continue
            sentences.append(line)
    return sentences



def get_sessions_by_file(data_set_file_path):
    """

    Parameters
    ----------
    data_set_file_path : str

    Returns
    -------

    """

    with open(data_set_file_path, 'r', encoding='UTF8') as reader:
        sessions = []
        session = []
        for line in reader.readlines():
            line = line.strip()
            if line == "":
                if len(session) > 0:
                    sessions.append(session)
                session = []
            else:
                session.append(line)
        if len(session) > 0:
            sessions.append(session)
    return sessions

def write_sessions_to_file(file_path, sessions):
    """

    Parameters
    ----------
    file_path : str
    sessions : list

    Returns
    -------

    """
    with open(file_path, 'w', encoding='UTF8') as writer:
        for session in sessions:
            for sentence in session:
                writer.write(sentence + '\n')
                #writer.write('\n'.join(session))
            writer.write('\n')


def make_train_dev_set(data_set_file_path, train_file_path, dev_file_path, train_rating=0.9):
    """

    Parameters
    ----------
    data_set_file_path : str
    train_file_path : str
    dev_file_path : str
    train_rating : float

    Returns
    -------

    """
    sessions = get_sessions_by_file(data_set_file_path)
    train_set, dev_set = get_traing_dev_set(sessions, train_rating)
    write_sessions_to_file(train_file_path, train_set)
    write_sessions_to_file(dev_file_path, dev_set)


def load_music_sentence(session_file_path):
    music_sentences = []
    with open(session_file_path, 'r', encoding='UTF8') as reader:
        for line in reader.readlines():
            line = line.strip()
            if line == '':
                continue
            find_music_index = line.find('music')
            if find_music_index != -1:
                splits = line.split('\t')
                sentence = splits[1]
                music_sentences.append(sentence)
    return music_sentences


def batch_segment(sentences, output_file_path):
    """

    Parameters
    ----------
    sentences :
    output_file_path :

    Returns
    -------

    """
    with open(output_file_path, 'w', encoding='UTF8') as writer:
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence == '':
                continue
            words = pseg.cut(sentence, HMM=False)
            result_format = [seg + '/' + pos for (seg, pos) in words]
            result_output = ' '.join(result_format)
            writer.write(str(result_output) + '\n')

def batch_segment_music(session_file_path, output_file_path):
    music_sentences = load_music_sentence(session_file_path)
    batch_segment(music_sentences, output_file_path)

def set_suggest_by_file(file_path):
    sentences = load_sentences_from_file(file_path)
    for sentence in sentences:
        splits = sentence.split(' ')
        if len(splits) == 2:
            jieba.suggest_freq((splits[0], splits[1]), True)



if __name__ == '__main__':

    '''
    data_file_path = '/Users/qiuxiaohu/codes/formalCode/competition/nlpcc/data/corpus.train.txt'
    train_file_path = './kami_train.txt'
    dev_file_path = './kami_dev.txt'
    make_train_dev_set(data_file_path, train_file_path, dev_file_path, 0.8)
    #music_seg_result = './dev_music_posseg.txt'
    #batch_segment_music(train_file_path, music_seg_result)

    '''
    suggest_file_path = os.path.join(local_dir, "../../data/jie_suggest.dic")

    set_suggest_by_file(suggest_file_path)

    jieba.load_userdict(os.path.join(local_dir, "../../data/userdict.txt"))
    seg_result = pseg.cut('我要听陈奕迅的烟味')
    jieba.suggest_freq(('摇滚', '音乐'), True)
    result_format = [seg + '/' + pos for (seg, pos) in seg_result]
    print(result_format)
    sentences_file = os.path.join(local_dir, "../../data/error_seg.txt")
    sentences = load_sentences_from_file(sentences_file)
    segment_file = os.path.join(local_dir, "../../data/error_seg_results.txt")
    batch_segment(sentences, segment_file)
