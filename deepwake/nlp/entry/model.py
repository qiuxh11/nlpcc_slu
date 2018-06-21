import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import thulac

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
        mod = __import__('deepwake.nlp.entry.feature', fromlist=['feature'])
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
        ''' 特征向量的长度

        Returns
        -------

        '''
        return self._length

    def info(self):
        return self._info


class Model:

    def __init__(self):
        self._model = svm.SVC(C=0.8, kernel='linear')
        self.feature_addition = None
        self.train_path = None
        self.corpus = None
        self.report = None

    def set_model(self, model):
        self._model = model

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

        self._model.fit(x_train, y_train.ravel())

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
        return self._model.coef_

    def predict(self, X):
        return self._model.predict(X)

    def feature_dim(self):
        return self.feature_addition.length()


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
    pass


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

