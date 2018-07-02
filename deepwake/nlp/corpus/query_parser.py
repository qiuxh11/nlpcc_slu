from deepwake.nlp.corpus.session import Query


class QueryParser():


    def parse(self, query):
        """

        Parameters
        ----------
        path

        Returns
        -------

        """
        pass


def angle_bracket_parse(label_record):
    """ 抽取标注语句的信息.

    Parameters
    ----------
    label_record: str
        labelled sentence.
    Returns
    -------
        [
         (label_0, value_0, (start_index, end_index)),
         (label_1, value_1, (start_index, end_index)),
         ....,
         ]
    """
    slot_values = []
    i = 0
    length = len(label_record)
    count = 0
    while i < length:
        if label_record[i] != '<':
            i += 1
            continue
        start_name = ''
        if i+1 < length and label_record[i] == '<' and label_record[i+1] != '/':
            j = i + 1
            while j < length and label_record[j] != '>':
                j += 1
            start_name = label_record[i+1:j]
            if j == length:
                break
            i = j + 1
            count += len(start_name) + 2
        try:
            end = "</" + start_name + ">"
            end_pos = str(label_record[i:]).index(end)
            value = label_record[i: i+end_pos]
            slot_values.append((start_name, value, (i-count, i+end_pos-count)))
            i = i + end_pos + len(end)
            count += len(end)
        except:
            return slot_values
    return slot_values


class NLPCCQueryParser(QueryParser):

    def parse(self, query):
        """

        Parameters
        ----------
        path:

        Returns
        -------
            Query.
        """
        fields = query.split()
        if len(fields) == 4:
            id = int(fields[0])
            sentence = fields[1]
            domain = fields[2].split('.')[0]
            intent = fields[2].split('.')[-1]
            slot_values = angle_bracket_parse(fields[3])
            query = Query(id, sentence, domain, intent, slot_values)
            return query
        return None

if __name__ == "__main__":
    res = angle_bracket_parse("播放<theme>dj</theme><theme>hello</theme>去<destination>牧香自助火锅</destination>")
    print(res)