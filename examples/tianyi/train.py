#encoding:utf-8
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
niter=40000
solver = caffe.SGDSolver('/home/clxia/caffe-master/models/SeNet/solver.prototxt')
solver.net.copy_from('/home/clxia/caffe-master/models/SeNet/SE-ResNeXt-101.caffemodel')
solver.solve()
for it in range(niter):
    solver.step(1)  # SGD by Caffe
    # store the train loss
    print 'ok'
    train_loss = solver.net.blobs['loss'].data
    if it % 100 == 0:  
       accuracy=solver.net.blobs['Accuracy'].data
       if accuracy>=0.99:
          snapshot()
    #    print 'iter %d, loss=%f, accuracy=%f' % (it,train_loss,accuracy)

print 'done'
