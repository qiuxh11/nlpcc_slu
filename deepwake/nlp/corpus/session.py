

class Query():
    DOMAIN_DICT = {}
    INTENT_DICT = {}
    DOMAIN_INDEX = 0
    INTENT_INDEX = 0

    def __init__(self, id, sentence, domain, intent, slot_values):
        self.session_id = id
        self.sentence = sentence

        self.domain = domain
        if domain not in Query.DOMAIN_DICT:
            Query.DOMAIN_DICT[domain] = Query.DOMAIN_INDEX
            Query.DOMAIN_INDEX += 1

        self.intent = intent
        if intent not in Query.INTENT_DICT:
            Query.INTENT_DICT[intent] = Query.INTENT_INDEX
            Query.INTENT_INDEX += 1

        self.slot_values= slot_values
        self.domain_id = Query.DOMAIN_DICT[self.domain]
        self.intent_id = Query.INTENT_DICT[self.intent]

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


