from flask import Flask, request, render_template, jsonify

import pickle
from keras.models import load_model, Model
import keras.backend as K
import tensorflow as tf
from pythainlp.tokenize import word_tokenize

import prediction

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

K.clear_session()
model = dict()
model['sunthorn'] = load_model('model/sunthorn_word.h5')
model['mix'] = load_model('model/mix_word.h5')
graph = tf.get_default_graph()

word_to_idx = dict()
idx_to_word = dict()

word_to_idx['sunthorn'] = pickle.load(open('dict/word_to_idx_sun.p', 'rb'))
word_to_idx['mix'] = pickle.load(open('dict/word_to_idx.p', 'rb'))
idx_to_word['sunthorn'] = pickle.load(open('dict/idx_to_word_sun.p', 'rb'))
idx_to_word['mix'] = pickle.load(open('dict/idx_to_word.p', 'rb'))

maxlen = 44


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict')
def _predict():
    method = request.args.get('method', default='greedy')
    style = request.args.get('style', default='sunthorn')
    temp = float(request.args.get('temp', default='1'))
    input_text = request.args.get('tok', default='')
    wak_limit = int(request.args.get('wak', default='4'))

    word_tokens = ['<s>']
    word_tokens.extend(word_tokenize(input_text))
    word_tokens = [x.strip() for x in word_tokens if x.strip() != '']

    for word in word_tokens:
        if word not in word_to_idx[style]:
            error_msg = 'Unknown vocabulary ' + word
            return jsonify(status='error', message=error_msg)

    if method == 'greedy':
        result_tokens = prediction.predict_greedy(
            word_tokens, maxlen, graph, model[style], word_to_idx[style], idx_to_word[style], wak_limit)
    elif method == 'temp':
        result_tokens = prediction.temperature_sampling_decode(
            word_tokens, maxlen, graph, model[style], word_to_idx[style], idx_to_word[style], temp, wak_limit)
    elif method == 'beam':
        result_tokens = prediction.beam_search_decode(
            word_tokens, maxlen, graph, model[style], word_to_idx[style], idx_to_word[style], maxlen, beam_size=5, wak_limit=wak_limit, normalized=True)

    result = prediction.format_output(result_tokens, wak_limit)
    print(result)
    return jsonify(status='ok', message=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
