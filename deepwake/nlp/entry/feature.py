from deepwake.nlp.entry.constant import TAB
from deepwake.nlp.entry.util import  WORD_DICT, DICT_FEATURE_INDEX


class Feature(object):

    def __init__(self):
        self._length = 1

    def active(self, text):
        """

        Parameters
        ----------
        text

        Returns
        -------

        """
        pass

    @property
    def length(self):
        return self._length


class NSFeature(Feature):

    def active(self, text):
        """

        Parameters
        ----------
        text

        Returns
        -------

        """
        score = 0.0
        for word in text:
            if word[1] == 'ns':
                score += 1
        return [score]

    def __str__(self):
        return 'ns特征'


class DictFeature(Feature):

    def __init__(self):
        super().__init__()

    def active(self, text):
        """

        Parameters
        ----------
        text

        Returns
        -------

        """
        vector = [0] * len(DICT_FEATURE_INDEX)
        for word in text:
            if word[0] in WORD_DICT.keys():
                name = WORD_DICT[word[0]]
                if name in DICT_FEATURE_INDEX.keys():
                    vector[DICT_FEATURE_INDEX[name]] += 1.0
        return vector

    @property
    def length(self):
        self._length = len(DICT_FEATURE_INDEX)
        return self._length

    def __str__(self):
        sorted_item = sorted(DICT_FEATURE_INDEX.items(), key=lambda d:d[1], reverse=False)
        res = ''
        for item in sorted_item:
            res = res + item[0] + TAB
        return res.strip()




