import tensorflow as tf
import codecs
# X=[[tf,idf,tfidf,tr,intitle,pos]......]
# Y=[0,1,1.....]


ranks= 6
topm = 10

totalsize=50

dataname="..\data\entityOutPut_originCut-pyltp_5006_datacache.txt"
f=codecs.open(dataname,'r','utf-8')
X=[]
Y=[]
dims=ranks+1
linenum=0
x_news=[]
yy=[]


for line in f.readlines():
    linenum+=1
    xx=[]
    data=line.strip().split(" ")
    for i in range(ranks):
        xx.append(data[i])
    x_news.append(xx)
    yy.append(data[ranks])
    if linenum%10==0:
        X.append(x_news)
        Y.append(yy)
        x_news=[]
        yy=[]

print(X)
print(Y)

x = tf.placeholder(tf.float32, shape=(topm, ranks), name="x-input")
y_ = tf.placeholder(tf.float32, shape=(10, None), name='y-input')

def get_weight(shape , lambdaa):
    var = tf.Variable(tf.random_normal(shape),dtype=tf.float32)
    tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(lambdaa)(var))
    return var



# layer_dimension=[2,1]
layer_dimension=[ranks,16,128,1024,512,topm]
n_layers=len(layer_dimension)

cur_layer = x
in_dimension = layer_dimension[0]

for i in range(1,n_layers):
    out_dimension = layer_dimension[i]
    weight = get_weight([in_dimension, out_dimension],0.001)
    bias = tf.Variable(tf.constant(0.1, shape=[out_dimension]))
    if i != n_layers-1:
        cur_layer = tf.nn.relu(tf.matmul(cur_layer, weight)+bias)
    else:
        cur_layer = tf.nn.sigmoid(tf.matmul(cur_layer, weight) + bias)
    in_dimension=layer_dimension[i]

y=cur_layer

if __name__ == '__main__':
    if __name__ == '__main__':
        cross_entropy_loss = -tf.reduce_mean(tf.multiply(y_,tf.log(y))+tf.multiply(1-y_,tf.log(1-y)))
    tf.add_to_collection('losses', cross_entropy_loss)

    loss = tf.add_n(tf.get_collection('losses'))
    train_step=tf.train.AdamOptimizer(0.001).minimize(loss)

    loss_result=[]

    print ('start training')

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        STEPS = 1000
        for i in range(STEPS):
            # start = (i*batch_size) % data_size
            # end = min(start+batch_size,data_size)
            # start=0
            # end=49
            # sess.run(train_step,feed_dict={x: X[start:end], y_:Y[start:end]})
            # if i%1000 == 0 :
            #     cur_loss = sess.run(loss,feed_dict={x: X[start:end], y_:Y[start:end]})
            #     print("After %d training steps , current loss is %g ."%(i,cur_loss))
            for j in range(totalsize):
                sess.run(train_step, feed_dict={x: X[j], y_: Y[j]})
                if i % 1000 == 0:
                    cur_loss = sess.run(loss, feed_dict={x: X[j], y_: Y[j]})
                    print("After %d training steps , current loss is %g ." % (i, cur_loss))





    tf.train.write_graph(sess.graph_def, '../tmp/my-model', 'train.pbtxt')
