#!/usr/bin/python
# -*- coding: utf-8 -*-
# import tensorflow as tf  
from numpy.random import RandomState  
import numpy as np
import math
import datetime
import time,os
from numpy import *
starttime = datetime.datetime.now()    
###################################
# 函数定义
def fun_tanh(x):
    y=(1.0-np.exp(-2.0*x))/(1.0+np.exp(-2.0*x))
    return y
def fun_sigmoid(x):
    y=1.0/(1.0+np.exp(-x))
    return y
def deep_learning_score(wb,x):
    # wb=[(w1,b1),(w2,b2),(w3,b3),(w4,b4)]
    x=mat(x)
    length=len(wb)
    for (w,b) in wb[:length-1]:
        x=fun_tanh(x*w+b)
    (w,b)=wb[-1] #输出层的结果
    y=fun_sigmoid(x*w+b)
    return y[0,0] #返回一个数,而不是矩阵

dictionary_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "dict-label.txt")
dictionary=[]
with open(dictionary_path, "r") as fin:
  for line in fin.readlines():
    line=unicode(line.strip(), "utf-8")
    dictionary.append(line)
print "There are %d keywords in the dictionary file!!!"%len(dictionary)

samples_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "test_200000")
fin=open(samples_path)
lines=fin.readlines()
row_num=len(lines) #文件的行数
col_num=len(dictionary)
print "There are %d lines in the input file!!!"%row_num

fout_path=os.path.join(os.path.split(os.path.realpath(__file__))[0], "uid_label_score.txt")
fout=open(fout_path,'w')

w1=np.loadtxt('w1.txt',delimiter=',')
w2=np.loadtxt('w2.txt',delimiter=',')
w3=np.loadtxt('w3.txt',delimiter=',')
w4=np.loadtxt('w4.txt',delimiter=',')
w5=np.loadtxt('w5.txt',delimiter=',')
w5=w5.reshape(-1,1) #(128L,)-->(128L,1)
# print w1.shape,w2.shape,w3.shape,w4.shape
# (6416L, 128L) (128L, 128L) (128L, 128L) (128L, 1L)
b1=np.loadtxt('b1.txt',delimiter=',')
b2=np.loadtxt('b2.txt',delimiter=',')
b3=np.loadtxt('b3.txt',delimiter=',')
b4=np.loadtxt('b4.txt',delimiter=',') #<type 'numpy.ndarray'>
b5=np.loadtxt('b5.txt',delimiter=',') 
wb=[(w1,b1),(w2,b2),(w3,b3),(w4,b4),(w5,b5)]

stat=dict()
# 字典初始化
interval=0.05
for start in arange(0,1.0,interval):
  end=start+interval
  key="[%.2f-%.2f)"%(start,end)
  stat[key]=[0,0]

for row,line in enumerate(lines): # row：0,1,2,3,...
  tmp_arr=np.zeros((1,col_num)) # 初始化(1L, 6416L) tmp_arr.dtype=float64
  line=unicode(line.strip(),'utf-8')
  uid,label,group_name,keywords,province,tier,head,tail,subroots=line.split(unicode(',','utf-8'))
  group_feature='group_'+group_name
  if group_feature in dictionary:
      index=dictionary.index(group_feature)
      tmp_arr[0,index]=1.0
  keyword_list=keywords.split(unicode(';','utf-8'))
  for keyword in keyword_list:
    if keyword in dictionary:
      index=dictionary.index(keyword)
      tmp_arr[0,index]=1.0
  subroot_list=subroots.split(unicode(';','utf-8'))
  for subroot in subroot_list:
    subroot_feature='subroot_'+subroot
    if subroot_feature in dictionary:
      index=dictionary.index(subroot_feature)
      tmp_arr[0,index]=1.0
  keyword_province='province_'+province
  keyword_tier='tier_'+tier
  keyword_head='head_'+head
  keyword_tail='tail_'+tail
  for keyword in [keyword_province,keyword_tier,keyword_head,keyword_tail]:
    if keyword in dictionary:
      index=dictionary.index(keyword)
      tmp_arr[0,index]=1.0
  x=tmp_arr
  y=deep_learning_score(wb,x)
  new_line="%s,%s,%.9f"%(uid,label,y)
  fout.write(new_line+'\n')
  #统计得分所在的分段
  for start in arange(0,1.0,interval):
    end=start+interval
    key="[%.2f-%.2f)"%(start,end)
    if start<=y<end:
      if label==u'0':
        stat[key][0]=stat[key][0]+1
      else:
        stat[key][1]=stat[key][1]+1
      break
  if row % 10000 == 0 :
    print "time:%s,row_no:%d"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),row) # 打印当前时间
fin.close()
fout.close()

score_stat_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "label_score_stat.csv")
fout=open(score_stat_path,'w')
for start in arange(0,1.0,interval):
  end=start+interval
  key="[%.2f-%.2f)"%(start,end)
  print key,stat[key][0],stat[key][1]
  line="%s,%d,%d"%(key,stat[key][0],stat[key][1])
  fout.write(line+'\n')
fout.close()
########################################
endtime = datetime.datetime.now()
print (endtime - starttime),"time used!!!" #0:00:00.280797
print "Finished!!!"
