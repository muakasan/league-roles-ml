import tensorflow as tf
import numpy as np

itemidToIndex = []
itemData = []

numItemIds = len(itemIdToIndex)

x = tf.placeholder(tf.int32, [None, numItemIds])

W = tf.Variable(tf.zeros([numItemIds]))
b = tf.Variable(tf.zeros([5]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.int32, [None, 5])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train(GradientDescentOptimizer(0.5).minimize(cross_entropy))

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

