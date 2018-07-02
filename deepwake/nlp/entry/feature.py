from deepwake.nlp.common.constant import TAB
from deepwake.nlp.common.loader import DICT_FEATURE_INDEX_DICT, WORD_LABEL_DICT


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
        vector = [0.0] * len(DICT_FEATURE_INDEX_DICT)
        for word in text:
            if word[0] in WORD_LABEL_DICT:
                for label in WORD_LABEL_DICT[word[0]]:
                    vector[DICT_FEATURE_INDEX_DICT[label]] += 1.0

        return vector

    @property
    def length(self):
        self._length = len(DICT_FEATURE_INDEX_DICT)
        return self._length

    def __str__(self):
        sorted_item = sorted(DICT_FEATURE_INDEX_DICT.items(),
                             key=lambda d:d[1], reverse=False)
        res = ''
        for item in sorted_item:
            res = res + item[0] + TAB
        return res.strip()




