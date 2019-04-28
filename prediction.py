
from keras.preprocessing.sequence import pad_sequences
import numpy as np


def format_output(word_tokens, wak_limit):
    output_text = []
    wak_count = 0
    for word in word_tokens:
        if word == '/':
            wak_count += 1
            if wak_count == 2:
                output_text.append('<br>')
            else:
                output_text.append(' ')
        elif word != '<s>' and word != '</s>':
            output_text.append(word)
    output_text = ''.join(output_text)
    return output_text


def tokens_to_sequences(tokens, word_to_index):
    seq = [word_to_index[tok] for tok in tokens]
    return seq


def predict_greedy(word_tokens, in_x, graph, model, word_to_idx, idx_to_word, wak_limit=4):
    with graph.as_default():
        wak_count = 0
        probs = []

        for _ in range(in_x):
            tmp = tokens_to_sequences(word_tokens, word_to_idx)
            tmp = pad_sequences([tmp], maxlen=in_x, value=0.0)

            pred = model.predict(tmp).flatten()
            output_idx = np.argmax(pred)
            probs.append(pred[output_idx])
            output_word = idx_to_word[output_idx]

            if output_word == '/':
                wak_count += 1
            if wak_count < wak_limit:
                word_tokens.append(output_word)
            else:
                break

        return word_tokens


def sample_output(probs, temperature=1.0):
    probs = np.power(probs, 1/temperature)
    probs = probs / np.sum(probs)
    np.random.seed(1)
    state = np.random.random()
    cum_probs = np.cumsum(probs)
    idx = np.searchsorted(cum_probs, state)
    return idx


def temperature_sampling_decode(word_tokens, in_x, graph, model, word_to_idx, idx_to_word, temperature, wak_limit=4):
    with graph.as_default():
        wak_count = 0
        probs = []

        for _ in range(in_x):

            indices = tokens_to_sequences(word_tokens, word_to_idx)
            indices = pad_sequences([indices], maxlen=in_x, padding='pre')

            pred = model.predict(indices).flatten()
            output_idx = sample_output(pred, temperature)
            probs.append(pred[output_idx])
            output_word = idx_to_word[output_idx]

            if output_word == '/':
                wak_count += 1
            if wak_count < wak_limit:
                word_tokens.append(output_word)
            else:
                break

        return word_tokens


def cal_score(score_list, length, normalized=False):

    seq_score = 0
    tmp_length = min(length, len(score_list))
    for i in range(length):

        seq_score += np.log(score_list[i] + 0.00000001)

    if(normalized):
        seq_score /= length

    return np.exp(seq_score)


def beam_search_decode(seed_tokens, max_gen_len, graph, model, word_to_index, index_to_word, max_sequence_len, beam_size, wak_limit=4, normalized=False):
    with graph.as_default():
        beams = [[seed_tokens, [], 0, 0]]

        for _ in range(max_gen_len):

            tmp_beams = beams.copy()
            beams = []
            for beam in tmp_beams:
                if(beam[0][-1] == "</s>"):
                    beams.append(beam)
                    continue

                if(beam[3] >= wak_limit):
                    beams.append(beam)
                    continue

                tmp = tokens_to_sequences(beam[0], word_to_index)
                tmp = pad_sequences([tmp], maxlen=max_sequence_len, value=0.0)

                output_word = model.predict(tmp).reshape(-1)
                top_beam_idx = np.argsort(output_word)[-1*beam_size:]
                top_beam_values = [output_word[i] for i in top_beam_idx]

                for i in range(beam_size):
                    tmp_beam_0 = beam[0] + [index_to_word[top_beam_idx[i]]]
                    tmp_beam_1 = beam[1] + [top_beam_values[i]]
                    tmp_beam_2 = beam[2] + 1
                    if index_to_word[top_beam_idx[i]] == '/':
                        tmp_beam_3 = beam[3] + 1
                    else:
                        tmp_beam_3 = beam[3]

                    beams.append(
                        [tmp_beam_0, tmp_beam_1, tmp_beam_2, tmp_beam_3])

            b_cal = []
            for beam in beams:
                b_cal.append(cal_score(beam[1], beam[2], normalized))
            top_beam_idx = np.argsort(b_cal)[-1*beam_size:]
            beams = [beams[x] for x in top_beam_idx]

        return beams[-1][0]
