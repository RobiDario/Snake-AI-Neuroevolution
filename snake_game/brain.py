import numpy as np

from config import INPUT_NEURONS,HIDDEN_NEURONS,OUTPUT_NEURONS
class NeuralNetwork:
    def __init__(self):

        self.weights_input_hidden = np.random.uniform(-1,1,(INPUT_NEURONS,HIDDEN_NEURONS))

        self.weights_hidden_output = np.random.uniform(-1,1,(HIDDEN_NEURONS,OUTPUT_NEURONS))

        self.bias_hidden= np.random.uniform(-1,1,(1,HIDDEN_NEURONS))
        self.bias_output = np.random.uniform(-1,1,(1,OUTPUT_NEURONS))

    def feed_forward(self, input_data):

        inputs=np.array(input_data).reshape(1,INPUT_NEURONS)

        hidden=np.dot(inputs,self.weights_input_hidden)+self.bias_hidden

        hidden=np.maximum(0,hidden)

        output=np.dot(hidden,self.weights_hidden_output)+self.bias_output

        return np.argmax(output)