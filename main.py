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
model['sunthorn'] = load_model('model/model.h5')
model['mix'] = load_model('model/model.h5')
graph = tf.get_default_graph()

word_to_idx = pickle.load(open('res/word_to_idx.p','rb'))
idx_to_word = pickle.load(open('res/idx_to_word.p','rb'))
in_x = 44

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def _predict():
     method =  request.args.get('method', default = 'greedy')
     style =  request.args.get('style', default = 'sunthorn')
     input_text = request.args.get('tok', default = '')
     wak_limit = int(request.args.get('wak', default = '4'))
     isMobile = (request.args.get('mobile', default = 'false')).lower() == 'true'

     word_tokens = ['<s>']
     word_tokens.extend(word_tokenize(input_text))

     for word in word_tokens:
          if word not in word_to_idx:
               error_msg = 'Unknown vocabulary ' + word
               return jsonify(status='error', message=error_msg)

     if method == 'greedy':
          result_tokens = prediction.predict_greedy(word_tokens, in_x, graph, model[style], word_to_idx, idx_to_word, wak_limit)
     elif method == 'beam':
          result_tokens = prediction.beam_search_decode(word_tokens, in_x, graph, model[style], word_to_idx, idx_to_word, in_x, 10, wak_limit, normalized=True)
     
     result = prediction.format_output(result_tokens,wak_limit,isMobile)      
     print(isMobile, result)
     return jsonify(status='ok', message=result)
     


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)