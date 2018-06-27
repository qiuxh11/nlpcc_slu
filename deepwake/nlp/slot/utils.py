from deepwake.nlp.corpus.query_parser import angle_bracket_parse


def convert_to_crf_format(sentence, intent, slot_values):
    words = sentence.words

    crf = []
    for word in words:
        crf.append(word[0] + '\t' + word[1] + '\t' + intent + '.O')

    if not slot_values:
        return crf

    slot_idx = 0
    slot_value = slot_values[slot_idx]
    temp = 0
    for idx, (word, pos, index) in enumerate(words):
        if index[0] < slot_value[2][0]:
            continue
        if index[1] < slot_value[2][1]:
            if temp == 0:
                crf[idx] = word + '\t' + pos + '\t' + intent + '.B'
                temp += 1
            else:
                crf[idx] = word + '\t' + pos + '\t' + intent + '.I'
            continue
        if index[1] == slot_value[2][1]:
            if temp == 0:
                crf[idx] = word + '\t' + pos + '\t' + intent + '.B'
            else:
                crf[idx] = word + '\t' + pos + '\t' + intent + '.E'
            slot_idx += 1
            if slot_idx < len(slot_values):
                slot_value = slot_values[slot_idx]
        else:
            return []
    return crf













