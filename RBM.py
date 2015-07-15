import numpy as np


class RBM():
    def __init__(self, data, num_hidden_units):
        self.num_visible_units = data.shape[1]
        self.num_hidden_units = num_hidden_units
        self.W = np.random.randn(self.num_hidden_units, self.num_visible_units)
        self.c = np.random.randn(self.num_hidden_units)
        self.b = np.random.randn(self.num_visible_units)

        self.fit(data)

    @classmethod
    def sigmoid(cls, vector):
        func = np.vectorize(cls.__sigmoid)
        return func(vector)

    @classmethod
    def __sigmoid(cls, x):
        return 1 / (1.0 + np.exp(-x))

    def fit(self, data, algorithm='sgd', learning_rate=1.0, epochs=10):
        if algorithm is 'sgd':
            self.__stochastic_gradient_descent(data, learning_rate, epochs)

    def transform(self):
        return

    def __stochastic_gradient_descent(self, data, learning_rate, iterations):
        for it in range(1, iterations + 1):
            np.random.shuffle(data)
            for sample in data:
                delta_W, delta_b, delta_c = self.__contrastive_divergence(sample)
                # W0 = np.copy(self.W)
                self.W = self.W + learning_rate * delta_W
                self.b = self.b + learning_rate * delta_b
                self.c = self.c + learning_rate * delta_c
                # diff = np.mean(np.abs(W0 - self.W))
                # print ">> Mean diff %f finished" % diff
            print ">> Epoch %d finished" % it

    def __contrastive_divergence(self, vector_visible_units, k=1):
        delta_W = np.zeros([self.num_hidden_units, self.num_visible_units])
        delta_b = np.zeros(self.num_visible_units)
        delta_c = np.zeros(self.num_hidden_units)
        v_0 = vector_visible_units
        v_t = np.copy(v_0)

        # Sampling
        for t in range(k):
            h_t = self.__compute_hidden_units(self.W, v_t, self.c)
            v_t = self.__compute_visible_units(self.W, h_t, self.b)

        # Computing deltas
        v_k = v_t
        h_0 = self.__compute_hidden_units(self.W, v_0, self.c)
        h_k = self.__compute_hidden_units(self.W, v_k, self.c)
        for i in range(self.num_hidden_units):
            for j in range(self.num_visible_units):
                delta_W[i][j] += h_0[i] * v_0[j] - h_k[i] * v_k[j]

        delta_b += v_0 - v_k
        delta_c += h_0 - h_k

        return delta_W, delta_b, delta_c

    def __compute_hidden_units(self, matrix_weights, vector_visible_units, vector_bias_hidden):
        W, v, c = matrix_weights, vector_visible_units, vector_bias_hidden
        return self.__sigmoid(np.dot(W, v) + c)

    def __compute_visible_units(self, matrix_weights, vector_hidden_units, vector_bias_visible):
        W, h, b = matrix_weights, vector_hidden_units, vector_bias_visible
        return self.__sigmoid(np.dot(h, W) + b)