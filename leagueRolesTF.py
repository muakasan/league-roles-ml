#Modified from https://github.com/joelgrus/fizz-buzz-tensorflow

import tensorflow as tf
import numpy as np

from leagueRoles import getRoleData

roleData = getRoleData()

numItemIds = len(roleData[0][1])

allX = np.array( list(map( lambda x: np.array(x[1]), roleData)))
allY = np.array( list(map( lambda x: np.array(x[0]), roleData)))

print(len(roleData))

trX = allX[:9000]
trY = allY[:9000]

vX = allX[9000:]
vY = allY[9000:]

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w_h, w_o):
    h = tf.nn.relu(tf.matmul(X, w_h))
    return tf.matmul(h, w_o)

X = tf.placeholder("float", [None, numItemIds])
Y = tf.placeholder("float", [None, 5])

NUM_HIDDEN = 10

w_h = init_weights([numItemIds, NUM_HIDDEN])
w_o = init_weights([NUM_HIDDEN, 5])

py_x = model(X, w_h, w_o)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y))
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost)

predict_op = tf.argmax(py_x, 1)

BATCH_SIZE = 128

with tf.Session() as sess:
    tf.initialize_all_variables().run()
    for epoch in range(3000):
        p = np.random.permutation(range(len(trX)))
        trX, trY = trX[p], trY[p]

        for start in range(0, len(trX), BATCH_SIZE):
            end = start + BATCH_SIZE
            sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end]})
        if epoch%100 == 0:
            print(epoch, np.mean(np.argmax(trY, axis=1) == sess.run(predict_op, feed_dict={X: trX, Y: trY})))
    sess.run(train_op, feed_dict={X: trX, Y: trY})
    print(np.mean(np.argmax(vY, axis=1) == sess.run(predict_op, feed_dict={X: vX, Y: vY})))

