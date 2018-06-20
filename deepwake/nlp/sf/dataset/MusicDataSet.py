import os
import jieba
import jieba.posseg as pseg
from taskbot.utils.utils import load_sentences_from_file


local_dir = os.path.dirname(os.path.realpath(__file__))

class MusicItem(object):

    def __init__(self, sentence, intent, semantic_slot_str):
        self.sentence = sentence
        self.intent = intent
        self.semantic_slot_str = semantic_slot_str
        self.semantic_slots = []
        self.is_valid_segment = False

class musicdataset(object):

    def make_data_crf_format(self, sessions_file_path, crf_output_file_path, error_segment_file_path):
        crf_writer = open(crf_output_file_path, 'w', encoding='UTF8')
        error_seg_writer = open(error_segment_file_path, 'w', encoding='UTF8')

        music_items = self.load_music_session_part(sessions_file_path)
        total_sentences = len(music_items)
        valid_segment_sentence = 0
        for music_item in music_items:
            slots = self._get_slots(music_item.sentence, music_item.semantic_slot_str)
            sentence_crf = self.get_sentence_of_crf(music_item.sentence, music_item.intent, slots)
            if sentence_crf != None:
                valid_segment_sentence = valid_segment_sentence + 1
                output_crf_sentence = [ word + '\t' + pos + '\t' + tag for (word, pos, tag) in sentence_crf]
                for output_crf in output_crf_sentence:
                    crf_writer.write(output_crf + '\n')
                crf_writer.write('\n')
            else:
                error_seg_writer.write(music_item.sentence + '\n')

        print('total sentence:%d, valid sentence:%d' % (total_sentences, valid_segment_sentence))

        error_seg_writer.close()
        crf_writer.close()



    def get_sentence_of_crf(self, sentence, intent, slots):
        words = pseg.cut(sentence)
        word_tuples = [(seg, pos) for (seg, pos) in words]
        print(len(word_tuples))
        sentence_crf = []
        for word in word_tuples:
            sentence_crf.append((word[0], word[1], intent + '.O'))

        for tuple in slots:
            start_index = tuple[0]
            slot_name = tuple[2]
            end_index = start_index + tuple[1]
            posseg_start_character_index = 0
            posseg_word_from_index = -1
            for i in range(len(word_tuples)):
                if posseg_start_character_index == start_index:
                    posseg_word_from_index = i
                    break
                posseg_start_character_index = posseg_start_character_index + len(word_tuples[i][0])
            if posseg_word_from_index == -1:
                print('word segment erorr....')
                print(word_tuples)
                print(slots)
                return None

            posseg_word_end_index = -1
            posseg_end_character_index = posseg_start_character_index
            for i in range(posseg_word_from_index, len(word_tuples)):
                posseg_end_character_index = posseg_end_character_index + len(word_tuples[i][0])

                if(posseg_end_character_index == end_index):
                    posseg_word_end_index = i
                    break
            if posseg_word_end_index == -1:
                print('word segment erorr....')
                print(word_tuples)
                print(slots)
                return None

            segment_len = posseg_word_end_index - posseg_word_from_index + 1
            sentence_crf[posseg_word_from_index] = (sentence_crf[posseg_word_from_index][0], sentence_crf[posseg_word_from_index][1], intent + '.' + slot_name + '-B')
            for i in range(posseg_word_from_index+1, posseg_word_end_index+1):
                sentence_crf[i] = (sentence_crf[i][0], sentence_crf[i][1], intent + '.' + slot_name + '-I')
        return sentence_crf


    def load_music_session_part(self, session_file_path):
        music_items = []
        with open(session_file_path, 'r', encoding='UTF8') as reader:
            for line in reader.readlines():
                line = line.strip()
                if line == '':
                    continue
                find_music_index = line.find('music')
                if find_music_index != -1:
                    splits = line.split('\t')
                    sentence = splits[1]
                    intent = splits[2].replace('music.', '').strip()
                    semantic_slot = splits[3].strip()
                    music_items.append(MusicItem(sentence, intent, semantic_slot))
        return music_items

    #来一首秧秧<singer>降央卓玛</singer>的<song>西海情歌</song>
    def _get_slots(self, sentence, semantic_slot_str):
        """
        
        Parameters
        ----------
        sentence : str
        semantic_slot_str : str

        Returns
        -------

        """
        semantic_slots = []
        from_find_index = 0
        sentence_index = 0
        find_bracet = semantic_slot_str.find('<', from_find_index)
        while find_bracet != -1:
            sentence_index = sentence_index + (find_bracet - from_find_index)
            find_right_bracet_index = semantic_slot_str.find('>', from_find_index)
            slot_name = semantic_slot_str[find_bracet+1:find_right_bracet_index]
            end_slot_sign = '</' + slot_name + ">"
            end_slot_index = semantic_slot_str.find(end_slot_sign, find_right_bracet_index+1)
            slot_value = semantic_slot_str[find_right_bracet_index+1:end_slot_index]
            find_db_name = slot_value.find('||')
            slot_value_len = end_slot_index - find_right_bracet_index - 1

            if find_db_name != -1:
                slot_value_len = find_db_name
                print('别名')
                print(semantic_slot_str)
                print(slot_value_len)


            semantic_slot_tuple = (sentence_index, slot_value_len, slot_name)
            sentence_index = sentence_index + slot_value_len
            semantic_slots.append(semantic_slot_tuple)
            from_find_index = end_slot_index + len(end_slot_sign)
            find_bracet = semantic_slot_str.find('<', from_find_index)

        return semantic_slots


def set_suggest_by_file(file_path):
    """

    Parameters
    ----------
    file_path : str

    Returns
    -------

    """
    sentences = load_sentences_from_file(file_path)
    for sentence in sentences:
        splits = sentence.split(' ')
        if len(splits) == 2:
            jieba.suggest_freq((splits[0], splits[1]), True)

if __name__=="__main__":
    jieba.load_userdict(os.path.join(local_dir, "../../data/userdict.txt"))
    suggest_file_path = os.path.join(local_dir, "../../data/jie_suggest.dic")

    #set_suggest_by_file(suggest_file_path)

    file_path = os.path.join(local_dir, "../../data/dev.txt")
    music_data_set = musicdataset()
    crf_output = os.path.join(local_dir, "../../data/crf_music_dev.txt")
    error_seg_file_path = os.path.join(local_dir, "../../data/dev_error_seg.txt")
    music_data_set.make_data_crf_format(file_path, crf_output, error_seg_file_path)


