import os

local_dir = os.path.dirname(os.path.realpath(__file__))

class SlotFillingReport(object):

    def __init__(self):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0
        self.right_sentence = 0
        self.total_sentence = 0
        self.sentence_accuracy = 0.0


class Evaluation(object):

    @staticmethod
    def write_predict_result(crf_predict_result, error_result_file_path):
        """

        Parameters
        ----------
        crf_predict_result :
        error_result_file_path :

        Returns
        -------

        """

        report_result = SlotFillingReport()

        real_tags = []
        predict_tags = []

        with open(error_result_file_path, 'w', encoding='UTF8') as writer:
            with open(crf_predict_result, 'r', encoding='UTF8') as reader:
                for line in reader.readlines():
                    line = line.strip()
                    if line == '':
                        writer.write('\n')
                        if len(real_tags) > 0:
                            report_result.total_sentence = report_result.total_sentence + 1
                            if Evaluation.is_sentence_predict_right(real_tags, predict_tags):
                                report_result.right_sentence = report_result.right_sentence + 1
                        real_tags = []
                        predict_tags = []
                    else:
                        splits = line.split('\t')
                        item_len = len(splits)
                        real_tags.append(splits[item_len-2])
                        predict_tags.append(splits[item_len-1])
                        if splits[item_len - 1] == splits[item_len - 2]:
                            writer.write(line + '\t' + 'right' + '\n')
                        else:
                            writer.write(line + '\t' + 'error' + '\n')

        report_result.sentence_accuracy = 1.0 * report_result.right_sentence / report_result.total_sentence
        return report_result

    @staticmethod
    def is_sentence_predict_right(real_tags, predict_tags):
        predict_right = True
        for i in range(len(real_tags)):
            if real_tags[i] != predict_tags[i]:
                predict_right = False
                break
        return predict_right


if __name__ == '__main__':

    train_result = os.path.join(local_dir, "../../data/predict_result/crf_music_train_result.txt")
    dev_result = os.path.join(local_dir, "../../data/predict_result/crf_music_dev_result_0529.txt")

    train_result_report = os.path.join(local_dir, "../../data/predict_result/crf_music_train_result_report.txt")
    dev_result_report = os.path.join(local_dir, "../../data/predict_result/crf_music_dev_result_report_0529.txt")

    #train_report = validate.write_predict_result(train_result, train_result_report)
    #print('train sentence right:%d, total:%d, accuracy:%f' % (train_report.right_sentence, train_report.total_sentence, train_report.sentence_accuracy))

    dev_report = Evaluation.write_predict_result(dev_result, dev_result_report)
    print('dev sentence right:%d, total:%d, accuracy:%f' % (dev_report.right_sentence, dev_report.total_sentence, dev_report.sentence_accuracy))





