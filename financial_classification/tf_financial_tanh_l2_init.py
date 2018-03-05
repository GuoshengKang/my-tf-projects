#!/usr/bin/python
# -*- coding: utf-8 -*-
import tensorflow as tf  
from numpy.random import RandomState  
import numpy as np
import math
import datetime
import time
starttime = datetime.datetime.now()    
###################################
# 参数设置
x_dim = 6416 # 样本数据的维度
unit_num = 128 # 每个隐层包含的神经元数
batch_size = 5000 # 定义每次训练数据batch的大小,防止内存溢出 
steps = 200000 # 设置神经网络的迭代次数 
top_percentage = 0.2 # 用于统计前%20得分的正负样本数
learning_rate = 0.02 # 学习率
###################################
Weight1=np.loadtxt('w1_v1.txt',delimiter=',')
Weight2=np.loadtxt('w2_v1.txt',delimiter=',')
Weight3=np.loadtxt('w3_v1.txt',delimiter=',')
Weight4=np.loadtxt('w4_v1.txt',delimiter=',')
Weight5=np.loadtxt('w5_v1.txt',delimiter=',')
Weight5=Weight5.reshape(-1,1) #(128L,)-->(128,1)
# print w1.shape,w2.shape,w3.shape,w4.shape
# (6416L, 128L) (128L, 128L) (128L, 128L) (128L, 1L)
Bias1=np.loadtxt('b1_v1.txt',delimiter=',')
Bias1=np.array([Bias1]) #(128L,)-->(1,128)
Bias2=np.loadtxt('b2_v1.txt',delimiter=',')
Bias2=np.array([Bias2]) #(128L,)-->(1,128)
Bias3=np.loadtxt('b3_v1.txt',delimiter=',')
Bias3=np.array([Bias3]) #(128L,)-->(1,128)
Bias4=np.loadtxt('b4_v1.txt',delimiter=',') #<type 'numpy.ndarray'>
Bias4=np.array([Bias4]) #(128L,)-->(1,128)
Bias5=np.loadtxt('b5_v1.txt',delimiter=',') 
Bias5=np.array([Bias5]) #(1,)-->(1,)
# print Bias1.shape, Bias2.shape, Bias3.shape, Bias4.shape, Bias5.shape
# (1, 128) (1, 128) (1, 128) (1, 128) (1,) 
##################################
#定义输入和输出  
x = tf.placeholder(tf.float32,shape=(None,x_dim),name="x-input")  
y = tf.placeholder(tf.float32,shape=(None,1),name="y-input")  

#定义神经网络的参数
#第一个隐层
w1 = tf.Variable(Weight1,dtype=tf.float32) #6235行,128列
b1 = tf.Variable(Bias1,dtype=tf.float32) # 1,128
z1 = tf.matmul(x, w1)+b1 # 
a1 = tf.nn.tanh(z1) #使用tanh函数作为激活函数
#第二个隐层
w2 = tf.Variable(Weight2,dtype=tf.float32) #128行128列
b2 = tf.Variable(Bias2,dtype=tf.float32) # 1,128
z2 = tf.matmul(a1, w2)+b2 # 
a2 = tf.nn.tanh(z2) #使用tanh函数作为激活函数
#第三个隐层
w3 = tf.Variable(Weight3,dtype=tf.float32) #10行10列
b3 = tf.Variable(Bias3,dtype=tf.float32) # 1,10
z3 = tf.matmul(a2, w3)+b3 # 
a3 = tf.nn.tanh(z3) #使用tanh函数作为激活函数
#第四个隐层
w4 = tf.Variable(Weight4,dtype=tf.float32) #10行10列
b4 = tf.Variable(Bias4,dtype=tf.float32) # 1,10
z4 = tf.matmul(a3, w4)+b4 # 
a4 = tf.nn.tanh(z4) #使用tanh函数作为激活函数

#定义神经网络输出层
w5 = tf.Variable(Weight5,dtype=tf.float32)
b5 = tf.Variable(Bias5,dtype=tf.float32)
z5 = tf.matmul(a4,w5) + b5
prediction = tf.nn.sigmoid(z5)

# 训练数据集 
X_train = np.load('100000_X_train.npy')   
print "train samples:",X_train.shape
y_train = np.load('100000_y_train.npy') 
train_num = y_train.shape[0]
top20_train = int(top_percentage*train_num)
y_train = y_train.reshape([train_num,1]) # 转成nx1数组
dataset_size=train_num # 训练样本数目

# 测试数据集
X_test = np.load('100000_X_test.npy')   
print "test samples:",X_test.shape
y_test = np.load('100000_y_test.npy') 
test_num = y_test.shape[0]
print y_test.shape
top20_test = int(top_percentage*test_num)
y_test = y_test.reshape([test_num,1]) # 转成nx1数组

# 定义损失函数,这里只需要刻画模型在训练数据上表现的损失函数
mse_loss = tf.reduce_mean(tf.square(y - prediction))
# 这个函数第一个参数是'losses'是集合的名字,第二个参数是要加入这个集合的内容
tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(0.001)(w1))
tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(0.001)(w2))
tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(0.001)(w3))
tf.add_to_collection('losses',tf.contrib.layers.l2_regularizer(0.001)(w4))
# 将均方误差损失函数加入损失集合
tf.add_to_collection('losses',mse_loss)
# 将集合中的元素加起来,得到最终的损失函数
loss=tf.add_n(tf.get_collection('losses'))

#定义反向传播算法的优化函数
# global_step=tf.Variable(0)
# decay_steps = int(math.ceil(train_num/batch_size)) #衰减速度
# decay_rate = 0.96 # 衰减系数
# learning_rate = tf.train.exponential_decay(0.1,global_step,decay_steps,decay_rate,staircase=True)
my_opt = tf.train.GradientDescentOptimizer(learning_rate)
train_step = my_opt.minimize(loss)

# 参数输出格式
fmt=['%.9f']
w1_fmt=unit_num*fmt
w2_fmt=unit_num*fmt
w3_fmt=unit_num*fmt
w4_fmt=unit_num*fmt
w5_fmt=fmt

#创建会话运行TensorFlow程序  
with tf.Session() as sess:  
    #初始化变量  tf.initialize_all_variables()  
    init = tf.initialize_all_variables()  
    sess.run(init)  
    for i in range(steps):  
        #每次选取batch_size个样本进行训练  
        start = (i * batch_size) % dataset_size  
        end = min(start + batch_size,dataset_size)
        #通过选取样本训练神经网络并更新参数  
        X_batch=X_train[start:end];y_batch=y_train[start:end]
        sess.run(train_step,feed_dict={x:X_batch,y:y_batch})  
        #每迭代100次输出一次日志信息  
        if i % 100 == 0 :
            print "time:%s,"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), # 打印当前时间
            # print "learning_rate:%0.6f,"%sess.run(learning_rate), # 打印学习率
            # 计算训练数据的损失之和  
            total_loss = sess.run(loss,feed_dict={x:X_batch,y:y_batch})  
            print "training_steps:%05d, total_loss:%0.6f,"%(i,total_loss),
            # 对训练数据进行预测
            # prediction_value = sess.run(prediction,feed_dict={x:X_batch}) # mx1
            # c= np.c_[y_batch,prediction_value] # 将标签和得分合在一个数组中
            # sorted_c=c[np.lexsort(-c.T)] # 按最后一列逆序排序
            # print "[%0.6f,%0.6f],"%(sorted_c[top20_train-1,1],sorted_c[0,1]),
            # positive_num=sum(sorted_c[:top20_train,0]);negative_num=top20_train-positive_num
            # print "positive_rate:%0.6f,"%(positive_num/top20_train),
            # prediction_label = np.array([[1 if p_value[0]>=0.5 else 0] for p_value in prediction_value]) # mx1
            # yes_no=(prediction_label==y_train)
            # print "prediction_accuracy:%0.6f on train data;"%(yes_no.sum()/float(train_num)),
            # 对测试数据进行预测
            prediction_value = sess.run(prediction,feed_dict={x:X_test}) # mx1
            c= np.c_[y_test,prediction_value] # 将标签和得分合在一个数组中
            sorted_c=c[np.lexsort(-c.T)] # 按最后一列逆序排序
            print "[%0.6f,%0.6f],"%(sorted_c[top20_test-1,1],sorted_c[0,1]),
            positive_num=sum(sorted_c[:top20_test,0]);negative_num=top20_test-positive_num
            print "positive_rate:%0.6f,"%(positive_num/top20_test),
            prediction_label = np.array([[1 if p_value[0]>=0.5 else 0] for p_value in prediction_value]) # mx1
            yes_no=(prediction_label==y_test)
            print "prediction_accuracy:%0.6f on test data"%(yes_no.sum()/float(test_num))
    #模型训练结束,输出和保存参数
    # print(w1.eval(session=sess)) 
    parameter_w1=w1.eval(session=sess)
    np.savetxt('w1.txt',parameter_w1,fmt=w1_fmt,delimiter=',') 
    parameter_b1=b1.eval(session=sess)
    np.savetxt('b1.txt',parameter_b1,fmt=w1_fmt,delimiter=',') 
    parameter_w2=w2.eval(session=sess)
    np.savetxt('w2.txt',parameter_w2,fmt=w2_fmt,delimiter=',') 
    parameter_b2=b2.eval(session=sess)
    np.savetxt('b2.txt',parameter_b2,fmt=w2_fmt,delimiter=',') 

    parameter_w3=w3.eval(session=sess)
    np.savetxt('w3.txt',parameter_w3,fmt=w3_fmt,delimiter=',') 
    parameter_b3=b3.eval(session=sess)
    np.savetxt('b3.txt',parameter_b3,fmt=w3_fmt,delimiter=',') 

    parameter_w4=w4.eval(session=sess)
    np.savetxt('w4.txt',parameter_w4,fmt=w4_fmt,delimiter=',') 
    parameter_b4=b4.eval(session=sess)
    np.savetxt('b4.txt',parameter_b4,fmt=w4_fmt,delimiter=',') 

    parameter_w5=w5.eval(session=sess)
    np.savetxt('w5.txt',parameter_w5,fmt=w5_fmt,delimiter=',') 
    parameter_b5=b5.eval(session=sess)
    np.savetxt('b5.txt',parameter_b5,fmt=w5_fmt,delimiter=',') 

endtime = datetime.datetime.now()
print (endtime - starttime),"time used!!!" #0:00:00.280797

print "Finished!!!"