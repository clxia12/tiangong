#encoding:utf-8
import numpy as np
import sys
import os
import cv2
import caffe
import csv
import time
import math
caffe_root = '/home/clxia/caffe-master/'
sys.path.insert(0, caffe_root + 'python')
caffe.set_mode_gpu()


#label0
net_file_label0 = '/home/clxia/caffe-master/models/ATAnet/ATAnet_test.prototxt'
caffe_model_label0 = '/home/clxia/caffe-master/models/ATAnet/solver_iter_60000_label0.caffemodel'
MWI_mean_file = '/home/clxia/caffe-master/data/tianyi/imagenet_mean.binaryproto'
print('Params loaded!')
net_label0 = caffe.Net(net_file_label0,
                caffe_model_label0,
                caffe.TEST)
#逆序label1
net_file_label1 = '/home/clxia/caffe-master/models/ATAnet/ATAnet_test.prototxt'
caffe_model_label1 = '/home/clxia/caffe-master/models/ATAnet/solver_iter_60000_label1.caffemodel'
net_label1 = caffe.Net(net_file_label1,
                caffe_model_label1,
                caffe.TEST)


#label2
net_file_label2 = '/home/clxia/caffe-master/models/ATAnet/ATAnet_test.prototxt'
caffe_model_label2 = '/home/clxia/caffe-master/models/ATAnet/solver_iter_60000_label2.caffemodel'
MWI_mean_file = '/home/clxia/caffe-master/data/tianyi/imagenet_mean.binaryproto'
print('Params loaded!')
net_label2 = caffe.Net(net_file_label2,
                caffe_model_label2,
                caffe.TEST)
#逆序label3
net_file_label3 = '/home/clxia/caffe-master/models/ATAnet/ATAnet_test.prototxt'
caffe_model_label3 = '/home/clxia/caffe-master/models/ATAnet/solver_iter_60000_label3.caffemodel'
net_label3 = caffe.Net(net_file_label3,
                caffe_model_label3,
                caffe.TEST)
#乱序label4
net_file_label4 = '/home/clxia/caffe-master/models/ATAnet/ATAnet_test.prototxt'
caffe_model_labe4 = '/home/clxia/caffe-master/models/ATAnet/solver_iter_60000_label4.caffemodel'
net_label4 = caffe.Net(net_file_label4,
                caffe_model_labe4,
                caffe.TEST)

mean_blob = caffe.proto.caffe_pb2.BlobProto()  # 创建protobuf blob
mean_blob.ParseFromString(open(MWI_mean_file, 'rb').read())    # 读入mean.binaryproto文件内容, # 解析文件内容到blob
mean_npy = caffe.io.blobproto_to_array(mean_blob) # 将blob中的均值转换成numpy格式，array的shape （mean_number，channel, hight, width）

#MWI :
#label0
a = mean_npy[0, :, 0, 0]
print(net_label0.blobs['data'].data.shape)
transformer_label0 = caffe.io.Transformer({'data': net_label0.blobs['data'].data.shape})
transformer_label0.set_transpose('data', (2, 0, 1))
transformer_label0.set_mean('data', a)
transformer_label0.set_raw_scale('data', 255.0)
transformer_label0.set_channel_swap('data', (2, 1, 0))

#逆序label1
print(net_label1.blobs['data'].data.shape)
transformer_label1= caffe.io.Transformer({'data': net_label1.blobs['data'].data.shape})
transformer_label1.set_transpose('data', (2, 0, 1))
transformer_label1.set_mean('data', a)
transformer_label1.set_raw_scale('data', 255.0)
transformer_label1.set_channel_swap('data', (2, 1, 0))

#label2
print(net_label2.blobs['data'].data.shape)
transformer_label2 = caffe.io.Transformer({'data': net_label2.blobs['data'].data.shape})
transformer_label2.set_transpose('data', (2, 0, 1))
transformer_label2.set_mean('data', a)
transformer_label2.set_raw_scale('data', 255.0)
transformer_label2.set_channel_swap('data', (2, 1, 0))

#逆序ｌａｂｅｌ3
print(net_label3.blobs['data'].data.shape)
transformer_label3= caffe.io.Transformer({'data': net_label3.blobs['data'].data.shape})
transformer_label3.set_transpose('data', (2, 0, 1))
transformer_label3.set_mean('data', a)
transformer_label3.set_raw_scale('data', 255.0)
transformer_label3.set_channel_swap('data', (2, 1, 0))
#乱序label4
print(net_label4.blobs['data'].data.shape)
transformer_label4 = caffe.io.Transformer({'data': net_label4.blobs['data'].data.shape})
transformer_label4.set_transpose('data', (2, 0, 1))
transformer_label4.set_mean('data', a)
transformer_label4.set_raw_scale('data', 255.0)
transformer_label4.set_channel_swap('data', (2, 1, 0))


#IALT
# ialt_mean_file = '/home/clxia/caffe-master/data/tianyi/ialt_imagenet_mean.binaryproto'
# ialt_mean_blob = caffe.proto.caffe_pb2.BlobProto()  # 创建protobuf blob
# ialt_mean_blob.ParseFromString(open(ialt_mean_file, 'rb').read())    # 读入mean.binaryproto文件内容, # 解析文件内容到blob
# ialt_mean_npy=caffe.io.blobproto_to_array(ialt_mean_blob)
# #IALT
# ialt=ialt_mean_npy[0,:,0,0]
# transformer_ialt = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# transformer_ialt.set_transpose('data', (2, 0, 1))
# transformer_ialt.set_mean('data', ialt)
# transformer_ialt.set_raw_scale('data', 255.0)
# transformer_ialt.set_channel_swap('data', (2, 1, 0))



# test_image_path='/home/clxia/caffe-master/data/test'
test_image_path='/home/clxia/Downloads/高度计数据集-预算训练集500/预赛训练集-500'

image_names=os.listdir(test_image_path)
image_names.sort()

ft=open('/home/clxia/caffe-master/data/res.txt','w')
# 写入csv文件，设置newline，否则两行之间会空一行
csvfile=open('/home/clxia/caffe-master/data/res-54.csv','w') 
#delimiter默认是逗号
writer=csv.writer(csvfile,delimiter=',')
#opposite label0
# names = ['DESERT', 'OCEAN', 'MOUNTAIN', 'FARMLAND', 'LAKE', 'CITY']
# 与原文label相反:1
# names_label1= ['CITY','LAKE','FARMLAND','MOUNTAIN','OCEAN','DESERT']
# 与原文label相反:2
names_label2= ['LAKE','FARMLAND','OCEAN','DESERT','CITY','MOUNTAIN']
# 与原文label相反:3
names_label3= ['CITY','MOUNTAIN','LAKE','FARMLAND','OCEAN','DESERT']
#与原文label相反　：４乱序
names_label4=['OCEAN','DESERT','CITY','MOUNTAIN','LAKE','FARMLAND']

imtonu={'LAKE':0,'FARMLAND':1,'OCEAN':2,'DESERT':3,'CITY':4,'MOUNTAIN':5}

pred=['LAKE','FARMLAND','OCEAN','DESERT','CITY','MOUNTAIN']
for image in image_names:
    start=time.clock()
    # img_path='/home/clxia/caffe-master/data/test/'+image
    img_path='/home/clxia/Downloads/高度计数据集-预算训练集500/预赛训练集-500/'+image
    im = caffe.io.load_image(img_path)
    #多光谱图
    # ig=cv2.imread(img_path)
    pre=[]

    if 'MWI' in image:
        #ＲＧＢ２gray
        img=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        im=cv2.merge([img,img,img])
        # size(256,256)lable0
        net_label0.blobs['data'].data[...] = transformer_label0.preprocess('data', im)
        predict_label0 = net_label0.forward()
        prob_label0 = net_label0.blobs['prob'].data[0].flatten()
        image_label_label0=names_label0[np.argmax(prob_label0)]
        pre.append(imtonu[image_label_label0])
        #label1
        net_label1.blobs['data'].data[...] = transformer_label1.preprocess('data', im)
        predict_label1 = net_label1.forward()
        prob_label1 = net_label1.blobs['prob'].data[0].flatten()
        image_label_label1=names_label1[np.argmax(prob_label1)]
        pre.append(imtonu[image_label_label1])

        # size(256,256)lable2
        net_label2.blobs['data'].data[...] = transformer_label2.preprocess('data', im)
        predict_label2 = net_label2.forward()
        prob_label2 = net_label2.blobs['prob'].data[0].flatten()
        image_label_label2=names_label2[np.argmax(prob_label2)]
        pre.append(imtonu[image_label_label2])
        #label3
        net_label3.blobs['data'].data[...] = transformer_label3.preprocess('data', im)
        predict_label3 = net_label3.forward()
        prob_label3 = net_label3.blobs['prob'].data[0].flatten()
        image_label_label3=names_label3[np.argmax(prob_label3)]
        pre.append(imtonu[image_label_label3])

        #label4
        net_label4.blobs['data'].data[...] = transformer_label4.preprocess('data', im)
        predict_label4 = net_label4.forward()
        prob_label4 = net_label4.blobs['prob'].data[0].flatten()
        image_label_label4=names_label4[np.argmax(prob_label4)]
        pre.append(imtonu[image_label_label4])

        image_label=pred[sorted(pre)[len(pre)/2]]
        ft.write(image+','+image_label+'\n')
        writer.writerow([image,image_label])
        # img=cv2.imread(img_path)
        # cv2.imwrite('/home/clxia/caffe-master/data/'+image_label+'/'+image,img)
        # break
    #微波图像
    if 'IALT' in image:

        net_label0.blobs['data'].data[...] = transformer_label0.preprocess('data', im)
        predict_label0 = net_label0.forward()
        prob_label0 = net_label0.blobs['prob'].data[0].flatten()
        image_label_label0=names_label0[np.argmax(prob_label0)]
        pre.append(imtonu[image_label_label0])
        #label1
        net_label1.blobs['data'].data[...] = transformer_label1.preprocess('data', im)
        predict_label1 = net_label1.forward()
        prob_label1 = net_label1.blobs['prob'].data[0].flatten()
        image_label_label1=names_label1[np.argmax(prob_label1)]
        pre.append(imtonu[image_label_label1])
        #label2
        net_label2.blobs['data'].data[...] = transformer_label2.preprocess('data', im)
        predict_label2 = net_label2.forward()
        prob_label2 = net_label2.blobs['prob'].data[0].flatten()
        image_label_label2=names_label2[np.argmax(prob_label2)]
        pre.append(imtonu[image_label_label2])
        #label3
        net_label3.blobs['data'].data[...] = transformer_label3.preprocess('data', im)
        predict_label3 = net_label3.forward()
        prob_label3 = net_label3.blobs['prob'].data[0].flatten()
        image_label_label3=names_label3[np.argmax(prob_label3)]
        pre.append(imtonu[image_label_label3])

        #
        net_label4.blobs['data'].data[...] = transformer_label4.preprocess('data', im)
        predict_label4 = net_label4.forward()
        prob_label4 = net_label4.blobs['prob'].data[0].flatten()
        image_label_label4=names_label4[np.argmax(prob_label4)]
        pre.append(imtonu[image_label_label4])

        image_label=pred[sorted(pre)[len(pre)/2]]
        ft.write(image+','+image_label+'\n')
        writer.writerow([image,image_label])


    elapsed=(time.clock()-start)
    print('time used:',elapsed)
ft.close()
csvfile.close()
