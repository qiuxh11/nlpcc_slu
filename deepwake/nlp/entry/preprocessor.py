from deepwake.nlp.common.constant import BIG_SEPARATOR
from deepwake.nlp.lang.sentence import Sentence


class Processor():

    def process(self, text):
        pass


class SplitProcessor(Processor):

    def process(self, text):
        processed_text = [element.strip() for element in text.split(BIG_SEPARATOR)]
        return processed_text

class SegProcessor(Processor):

    def process(self, text):
        sen = Sentence(text)
        sen.cut()
        return sen.words