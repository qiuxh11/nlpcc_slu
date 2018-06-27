
class Query():

    def __init__(self, id, sentence, domain, intent, slot_values):
        self.session_id = id
        self.sentence = sentence
        self.domain = domain
        self.intent = intent
        self.slot_values= slot_values

    def __str__(self):
        return str(self.session_id) + '\t' + str(self.sentence) + '\t' + str(self.domain) + '\t' \
               + str(self.intent) + '\t' + str(self.slot_values)

class Session():

    def __init__(self, session, ID=0):
        self.queries = []
        self.ID = ID
        self._session = session

    def parse_queries(self, query_parser):
        """ 将原始的标注session语句parse所需要的信息.

        Parameters
        ----------
        query_parser: QueryParser
            query解析器.

        Returns
        -------

        """
        for sess in self._session:
            query = query_parser.parse(sess)
            if query:
                self.ID = query.session_id
                self.queries.append(query)
        return self.queries

    def __iter__(self):
        return self.queries

    def __str__(self):
        res = ''
        for query in self.queries:
            res += str(query) + '\n'
        return res


