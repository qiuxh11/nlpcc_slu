import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import thulac

from deepwake.nlp.entry.constant import DOMAIN_REVERSE_DICT
from deepwake.nlp.entry.util import get_absolute_path, CONFIG, load_train_corpus
from deepwake.nlp.logger.log import Logger

SEG = thulac.thulac(user_dict=get_absolute_path("./dict/thulac.dict"))


class FeatureAddition(object):

    def __init__(self):
        self.features = []
        self._length = 0
        self._info = []

    def config(self, feature_names):
        """ 根据配置文件配置特征列表.

        Returns
        -------

        """
        mod = __import__('kami.nlp.entry.feature', fromlist=['feature'])
        for feature_name in feature_names:
            class_name = getattr(mod, feature_name)
            feature = class_name()
            self._length += feature.length
            self._info.append(str(feature))
            self.features.append(feature)

    def generate(self, text):
        vector = []
        for feature in self.features:
            vector = vector + feature.active(text)
        return vector

    def length(self):
        return self._length

    def info(self):
        return self._info


class TopicModel:

    def __init__(self):
        self._topic_model = svm.SVC(C=0.8, kernel='linear')
        self.feature_addition = None
        self.train_path = None
        self.corpus = None
        self.report = None

    def set_model(self, model):
        self._topic_model = model

    def set_feature_addition(self, feature_addition):
        self.feature_addition = feature_addition

    def load_train_corpus(self, path_dict):
        """ 载入训练语料.

        Parameters
        ----------
        path_dict

        Returns
        -------

        """
        self.corpus = load_train_corpus(path_dict)
        return self.corpus

    def generate(self, text):
        return self.feature_addition.generate(text)

    def create_train_data(self, path, label_dict):
        """ 创建训练数据特征集合.

        Parameters
        ----------
        path:
        label_dict: dict
            类别词典.

        Returns
        -------

        """
        self.train_path = get_absolute_path(path)
        data = []
        for name, queries in self.corpus.items():
            for query in queries:
                text = SEG.cut(query)
                vector = self.generate(text)
                if name in label_dict.keys():
                    vector.append(label_dict[name])
                    data.append(vector)
        arr = np.array(data)
        np.savetxt(self.train_path, arr, fmt='%.3f')#, header=self.feature_addition.info())

    def train_and_test(self, label_dict, train_size=0.7):
        data = np.loadtxt(self.train_path, dtype=float, delimiter=' ')
        x, y = np.split(data, (self.feature_addition.length(),), axis=1)
        x = x[:, :self.feature_addition.length()]
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=train_size)

        self._topic_model.fit(x_train, y_train.ravel())

        y_predict = self.predict(x_test)
        y_true = (y_test.reshape(y_test.shape[1], y_test.shape[0]))[0]

        label_names = sorted(label_dict.items(), key=lambda d:d[1])

        labels = []
        names = []
        for label in label_names:
            labels.append(label[1])
            names.append(label[0])
        self.report = classification_report(y_true, y_predict,
                                    labels=labels, target_names=names)

        print(self.report)
        return self._topic_model.coef_

    def predict(self, X):
        return self._topic_model.predict(X)

    def feature_dim(self):
        return self.feature_addition.length()


DOMAIN_MODEL = TopicModel()
DOMAIN_FEATURE_ADDITION = FeatureAddition()
DOMAIN_FEATURE_ADDITION.config(CONFIG['domain_feature'])
DOMAIN_MODEL.set_feature_addition(DOMAIN_FEATURE_ADDITION)
DOMAIN_MODEL.load_train_corpus(CONFIG['domain_train_corpus'])
DOMAIN_MODEL.create_train_data(CONFIG['domain_train_data'], DOMAIN_REVERSE_DICT)
DOMAIN_MODEL.train_and_test(DOMAIN_REVERSE_DICT)

# INTENT_MODEL = TopicModel()
# INTENT_FEATURE_ADDITION = FeatureAddition()
# INTENT_FEATURE_ADDITION.config(CONFIG['intent_feature'])
# INTENT_MODEL.set_feature_addition(INTENT_FEATURE_ADDITION)
# INTENT_MODEL.load_train_corpus(CONFIG['intent_train_corpus'])
# INTENT_MODEL.create_train_data(CONFIG['intent_train_data'])
# INTENT_MODEL.train_and_test()


def get_domain(sentence, response=None, register=None):
    """ 获得对话的域: 火车, 飞机, 酒店, 闲聊等域

    Parameters
    ----------
    sentence: str
        用户对话.

    Returns
    -------
        域的类别:TOPIC_DICT = {0: "traffic",
         1: "hotel",
         2: "chat",
         3: "train",
         4: "flight"}
    """
    text = SEG.cut(sentence)  # 进行一句话分词
    X = DOMAIN_MODEL.generate(text)
    vector = np.ndarray(shape=(1, DOMAIN_MODEL.feature_dim()))
    for idx, value in enumerate(X):
        vector[0, idx] = value
    return DOMAIN_MODEL.predict(vector)


def get_intent(sentence, response, register):
    """ 获得意图

    Parameters
    ----------
    sentence
    response
    register
    manager
    policy

    Returns
    -------

    """
    pass


def load_model(path):
    """

    Parameters
    ----------
    path

    Returns
    -------

    """
    pass


if __name__ == '__main__':
    sentence = '预定今天下午的机票'
    res = get_domain(sentence)
    print(res)
    logger = Logger(__name__)
    logger.info("hello")

