import numpy as np
import time

# Input the dimension of layers. The dimension that is a list containing the amount of unit of each layer.
# Output the random initializing parameters containing W and b.
def initialize_parameters(layers_dims):
    np.random.seed(round(time.time()))
    parameters = {}
    L = len(layers_dims)
    for l in range(1, L):
        parameters['W'+str(l)] = np.random.randn(layers_dims[l], layers_dims[l-1]) * 0.01
        parameters['b'+str(l)] = np.zeros(shape=(layers_dims[l], 1))
    return parameters
print(initialize_parameters([6,3,1]))


def linear_activation_forward(A_prev, W, b, activation):
    if(activation == 'sigmoid'):
        Z, linear_cache = linear_forward(A_prev,W,b)
        A, activation_cache = sigmoid(Z)
    elif(activation == 'relu'):
        Z, linear_cache = linear_forward(A_prev,W,b)
        A, activation_cache = relu(Z)
    cache = (linear_cache, activation_cache)
    return A, cache

def linear_forward(A, W, b):
    Z = np.dot(A, W) + b
    cache = (A, W, b)
    return Z, cache

def sigmoid(z):
    return 1. / (1 + np.exp(-z)), z

def relu(z):
    return np.maximum(0, z), z

def L_layer_forward(X, parameters):
    caches = []
    A = X
    L = len(parameters) // 2
    for i in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters['W'+str(l)], parameters['b'+str(l)], 'relu')
        caches.append(cache)
    AL, cache = linear_activation_forward(A, parameters['W'+str(L)], parameters['b'+str(L)], 'sigmoid')
    caches.append(cache)
    return AL, caches


def compute_cost(AL, Y):
    m = Y.shape[1]
    cost = (-1/m) * np.sum(Y*np.log(AL)+(1-Y)*np.log(1-AL))
    cost = np.squeeze(cost)
    return cost


def linear_activation_backward(dA, cache, activation):
    linear_cache, activation_cache = cache
    if(activation == 'relu'):
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    elif(activation == 'sigmoid'):
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    return dA_prev, dW, db

def linear_backward(dZ, cache):
    A_prev, W, b = cache
    m = A_prev.shape[1]
    dW = (1/m) * np.dot(dZ, A_prev.T)
    db = (1/m) * np.sum(dZ,axis=1,keepdims=True)
    dA_prev = np.dot(W.T, dZ)
    return dA_prev, dW, db


def sigmoid_backward(dA, Z):
    S = sigmoid(Z)
    dS = S * (1 - S)
    return dA * dS

def relu_backward(dA, Z):
    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0
    return dZ

def L_model_backward(AL, Y, cahces):
    grads = {}
    L = len(caches)
    m = AL.shape[1]
    Y = Y.reshape(AL.shape)
    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    current_cache = caches[L - 1]
    grads["dA" + str(L)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache,
                                                                                                  activation = "sigmoid")
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 2)], current_cache,
                                                                    activation = "relu")
        grads["dA" + str(l + 1)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp
    return grads

def update_parameters(parameters, grads, learning_rate):
     L = len(parameters) // 2
     for l in range(L):
        parameters["W" + str(l + 1)] = None
        parameters["b" + str(l + 1)] = None
     return parameters