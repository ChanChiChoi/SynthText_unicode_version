import argparse
import os
import glob
import os.path as osp
import numpy as np
import tensorflow as tf
#from matplotlib import pyplot as plt
from PIL import Image
import h5py

import models

def predict(model_data_path, imgpaths):

    
    # Default input size
    height = 228
    width = 304
    channels = 3
    batch_size = 1
   

   
    # Create a placeholder for the input image
    input_node = tf.placeholder(tf.float32, shape=(None, height, width, channels))

    # Construct the network
    net = models.ResNet50UpProj({'data': input_node}, batch_size, 1, False)
        
    with tf.Session() as sess:

        # Load the converted parameters
        print('Loading the model')

        # Use to load from ckpt file
        saver = tf.train.Saver()     
        saver.restore(sess, model_data_path)

        # Use to load from npy file
        #net.load(model_data_path, sess) 
        preds = []
        for imgpath in imgpaths:
            # Read image
            img = Image.open(imgpath)
            img = img.resize([width,height], Image.ANTIALIAS)
            img = np.array(img).astype('float32')
            img = np.expand_dims(np.asarray(img), axis = 0)
            # Evalute the network for the given image
            pred = sess.run(net.get_output(), feed_dict={input_node: img})
            preds.append([osp.basename(imgpath),pred])
            # Plot result
            #fig = plt.figure()
            #ii = plt.imshow(pred[0,:,:,0], interpolation='nearest')
            #fig.colorbar(ii)
            #plt.show()
            
        return preds
        
def save_h5(preds,output_path):
    outh5 = h5py.File(osp.join(output_path,'depth.h5'),'w')                
    outh5.create_group('/depth')
    for imgname,pred in preds:
        outh5['depth'].create_dataset(imgname,data = pred)
    outh5.close()

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', help='Converted parameters for the model')
    parser.add_argument('--image_paths', help='Directory of images to predict')
    parser.add_argument('--output_path', help='Directory of depth prediction of  images')
    parser.add_argument('--img_type', help='type of image')
    args = parser.parse_args()

    imgtype = '.jpg' if not args.img_type else '.'+args.img_type
    imgpaths = [args.image_paths] if osp.isfile(args.image_paths) else \
             glob.glob(osp.join(args.image_paths,'*{}'.format(imgtype)))
    # Predict the image
    preds = predict(args.model_path, imgpaths)
    save_h5(preds,args.output_path)
    os._exit(0)

if __name__ == '__main__':
    # python predict.py --model_path ../ckpt/NYU_FCRN.ckpt --image_paths ../../../data/bgi --img_type jpg --output_path ../depth
    main()

        



