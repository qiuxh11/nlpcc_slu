
class Query():

    def __init__(self, record):
        # 领域（音乐， 交通， 导航等）
        self.domain = None
        # 领域下的意图
        self.intent = None
        # 一句对话内容
        self.sentence = None
        # 标注的抽取信息.
        self.info = {}
        # 会话ID
        self.session_id = 0

    def set_parser(self, query_parser):
        pass


    def action(self):
        pass
