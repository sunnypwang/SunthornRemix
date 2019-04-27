from flask import Flask, request, render_template

import pickle
from keras.models import load_model, Model
import keras.backend as K
import tensorflow as tf
from pythainlp.tokenize import word_tokenize

import prediction

app = Flask(__name__)

K.clear_session()
model = load_model('model/model.h5')
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
    input_text = request.args.get('tok', default = '')
    wak_limit = int(request.args.get('wak', default = '4'))
    isMobile = (request.args.get('mobile', default = 'false')).lower() == 'true'
    
    word_tokens = ['<s>']
    word_tokens.extend(word_tokenize(input_text))
    
    if method == 'greedy':
         result_tokens = prediction.predict_greedy(word_tokens,in_x,graph,model,word_to_idx,idx_to_word,wak_limit)
    elif method == 'beam':
         result_tokens = prediction.beam_search_decode(word_tokens, in_x, graph, model, word_to_idx, idx_to_word, in_x, 10, wak_limit, normalized=True)
    result = prediction.format_output(result_tokens,wak_limit,isMobile)      
    print(isMobile, result)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)