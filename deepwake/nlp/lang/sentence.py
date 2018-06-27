import jieba.posseg

class Sentence():

    def __init__(self, sentence, seg=None):
        self.sentence = sentence
        self._words = None
        self.seg = seg

    def cut(self, seg=jieba.posseg):
        self._words = seg.cut(self.sentence)
        self.seg = seg
        words = []
        index = 0
        for (word, pos) in self._words:
            words.append((word, pos, (index, index+len(word))))
            index += len(word)
        del self._words
        self._words = words
        return self._words

    @property
    def words(self):
        return self._words
