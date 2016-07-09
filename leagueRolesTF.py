import tensorflow as tf
import numpy as np

from leagueRoles import getRoleData

roleData = getRoleData()

#print(roleData[:10])

#itemidToIndex = []
#itemData = []

#numItemIds = len(itemIdToIndex)
numItemIds = len(roleData[0][1])

'''
x = tf.placeholder(tf.int32, [None, numItemIds])

W = tf.Variable(tf.zeros([numItemIds, 5]))
b = tf.Variable(tf.zeros([5]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.int32, [None, 5])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train(GradientDescentOptimizer(0.5).minimize(cross_entropy))

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)
'''
allX = np.array( list(map( lambda x: np.array(x[1]), roleData)))
allY = np.array( list(map( lambda x: np.array(x[0]), roleData)))

#allX = map( lambda x: np.array(x[1]), roleData)
#allY = map( lambda x: np.array(x[0]), roleData)

print(len(roleData))

trX = allX[:800]
trY = allY[:800]

vX = allX[800:]
vY = allY[800:]

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w_h, w_o):
    h = tf.nn.relu(tf.matmul(X, w_h))
    return tf.matmul(h, w_o)

X = tf.placeholder("float", [None, numItemIds])
Y = tf.placeholder("float", [None, 5])

NUM_HIDDEN = 100

w_h = init_weights([numItemIds, NUM_HIDDEN])
w_o = init_weights([NUM_HIDDEN, 5])

py_x = model(X, w_h, w_o)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y))
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost)

predict_op = tf.argmax(py_x, 1)

with tf.Session() as sess:
    tf.initialize_all_variables().run()

    sess.run(train_op, feed_dict={X: trX, Y: trY}) #is this problematic?
    print(np.mean(np.argmax(vY, axis=1) == sess.run(predict_op, feed_dict={X: vX, Y: vY})))

