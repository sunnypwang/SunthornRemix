from flask import Flask, request
import pickle
import numpy as np
from keras.models import load_model, Model
from keras.preprocessing.sequence import pad_sequences
import keras.backend as K
import tensorflow as tf
import re

app = Flask(__name__)

K.clear_session()
model = load_model('model/model.h5')
graph = tf.get_default_graph()

word_to_idx = pickle.load(open('res/word_to_idx.p','rb'))
idx_to_word = pickle.load(open('res/idx_to_word.p','rb'))

def texts_to_sequences(text, word_to_index):
    text = text.strip().split()
    token_list = [word_to_index[x] for x in text]
    return token_list

@app.route('/')
def index():
    return 'Hello World'

@app.route('/predict')
def predict():
    global graph
    with graph.as_default():
        in_x = 44
        current_text = request.args.get('text', default = 'ฝ่าย')
        current_text = "<s> " + current_text
        probs = []
        for _ in range(in_x):
            tmp = texts_to_sequences(current_text, word_to_idx)
            tmp = pad_sequences([tmp], maxlen=in_x, value=0.0)

            output_word = model.predict(tmp)
            probs.append(output_word.max())
            output_word = np.argmax(output_word)
            output_word = idx_to_word[output_word]

            current_text += " " + output_word
        current_text = re.sub(r'\<\/*s\> ','',current_text)
        print(current_text)
        return current_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)