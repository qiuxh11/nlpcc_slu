import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import thulac

from deepwake.nlp.common.utils import get_absolute_path, load_corpus
from deepwake.nlp.corpus.session import Query
from deepwake.nlp.entry.feature import Feature

SEG = thulac.thulac()


class FeatureAddition(Feature):

    def __init__(self):
        super().__init__()
        # 特征列表.
        self.features = []
        # 语料预处理器.
        self.processors = []
        # 特征总维度.
        self._length = 0
        # 特征详细信息.
        self._info = []

    def config(self, feature_names, processor_names):
        """ 根据配置文件配置特征列表.

        Returns
        -------

        """
        mod = __import__('feature', fromlist=['feature'])
        for feature_name in feature_names:
            class_name = getattr(mod, feature_name)
            feature = class_name()
            self._length += feature.length
            self._info.append(str(feature))
            self.features.append(feature)

        mod = __import__('preprocessor', fromlist=['preprocessor'])
        for processor_name in processor_names:
            class_name = getattr(mod, processor_name)
            processor = class_name()
            self.processors.append(processor)


    def active(self, text):

        vector = []

        # 预处理.
        for processor in self.processors:
            text = processor.process(text)
        # 激活特征.
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
        self.domain_index_dict = {}
        self.index_domain_dict = {}

    def set_model(self, model):
        self._model = model

    def set_feature_addition(self, feature_addition):
        self.feature_addition = feature_addition

    def active_features(self, text):
        return self.feature_addition.active(text)

    def predict_big_data(self, corpus_path, predict_path_dict):
        out_paths = []
        for i in range(len(self.index_domain_dict)):
            domain = self.index_domain_dict[i]
            path = predict_path_dict[domain]
            file = open(path, 'w')
            out_paths.append(file)

        with open(corpus_path, mode='r') as reader:
            for line in reader:
                temp = line.strip()
                if temp == '':
                    continue
                sample = self.active_features(temp)
                sample = np.array([sample])
                res = self.predict(sample)
                if res[0] in self.index_domain_dict:
                    out_paths[int(res[0])].write(temp + '\n')

        for out in out_paths:
            out.close()

    def create_train_data(self, corpus,  train_path, domain=True):
        """ 创建训练数据特征集合.

        Parameters
        ----------
        corpus_path_dict:
        train_path: dict
            类别词典.

        Returns
        -------

        """
        self.train_path = get_absolute_path(train_path)
        self.corpus = corpus
        sessions = corpus.sessions

        data = []
        for session in sessions:
            temp = []
            history_vector = [0.0] * (self.feature_addition.length() + 1)
            for query in session.queries:
                current_vector = self.active_features(query.sentence)
                _vector = self._add(history_vector, current_vector)

                if domain:
                    _vector.append(query.domain_id)
                else:
                    _vector.append(query.intent_id)
                temp.append(_vector)
                history_vector = _vector
            for tmp in temp:
                data.append(tmp)
        arr = np.array(data)
        print(arr)
        np.savetxt(self.train_path, arr, fmt='%.3f')#, header=self.feature_addition.info())

    def train_and_test(self, domain_index_dict, train_size=0.6):
        data = np.loadtxt(self.train_path, dtype=float, delimiter=' ')
        x, y = np.split(data, (self.feature_addition.length(),), axis=1)
        x = x[:, :self.feature_addition.length()]
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=train_size)

        self._model.fit(x_train, y_train.ravel())

        y_predict = self.predict(x_test)
        y_true = (y_test.reshape(y_test.shape[1], y_test.shape[0]))[0]

        label_names = sorted(domain_index_dict.items(), key=lambda d:d[1])

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

    def _add(self, a, b):
        c = []
        for idx, d in enumerate(a):
            if idx == len(a) - 1:
                break
            c.append(a[idx] + b[idx])
        return c


