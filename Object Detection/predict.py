from cgi import test

from cv2 import threshold
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
from mmdet.core import get_classes
import mmcv
import matplotlib.pyplot as plt
import argparse
import os
import random
import cv2
import json
import torch
import time
import numpy as np
from PIL import Image
from shapely.geometry import Polygon

device = "cuda:0" if torch.cuda.is_available() else "cpu"

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=1, help="how many times to do inference")
parser.add_argument("--dir", type=str, default="visualResults", help="folder to save visual results")
parser.add_argument("--name", type=str, default="", help="specific image u want to test (put in data/random/test) [count=1]")
parser.add_argument("--type", type=str, default="img", help="type of inference (img / video)")
args = parser.parse_args()

# CHANGE THESE PARAMETERS AS NEEDED
# - Specify the path to model config and checkpoint file
config_file = 'configs/ours/fasterRcnn.py'
checkpoint_file = 'exps/exp3_F/epoch_12.pth'
# - Data sub-directory name
subdir = '1027data'
# - Threshold
thred = 0.4 #show predict bbox with probability above this
# - Overlap
minOverlap = 0.05 #at least 5%

if not os.path.exists(os.getcwd()+"/"+args.dir):
    os.mkdir(os.getcwd()+"/"+args.dir)

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device=device)

if args.type == "img":
    if args.name != "":
        img = f'data/{subdir}/test/{args.name}'
        im = Image.open(img)
        result = inference_detector(model, img)

        bbox_result = result
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)\
            for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)
        bboxes = np.vstack(bbox_result)
        labels_impt = np.where(bboxes[:, -1] > thred)[0]

        classes = ['tree','house']
        labels_impt_list = [labels[i] for i in labels_impt]
        labels_class = [classes[i] for i in labels_impt_list]
        
        treeInd = [i for i in range(len(labels_impt_list)) if labels_impt_list[i] == 0]
        houseInd = [i for i in range(len(labels_impt_list)) if labels_impt_list[i] == 1]

        trees = [] #[(left,top,right,bottom)]
        houses = []

        for ind in treeInd:
            left = bboxes[labels_impt][ind][0]
            top = bboxes[labels_impt][ind][1]
            right = bboxes[labels_impt][ind][2]
            bottom = bboxes[labels_impt][ind][3]
            trees.append((left, top, right, bottom))
        for ind in houseInd:
            left = bboxes[labels_impt][ind][0]
            top = bboxes[labels_impt][ind][1]
            right = bboxes[labels_impt][ind][2]
            bottom = bboxes[labels_impt][ind][3]
            houses.append((left, top, right, bottom))
        print("trees", trees)
        print("houses", houses)

        cleaning = False
        maxOverlap = 0.0

        for tree in trees:
            for house in houses:
                x1t,y1t,x2t,y2t = tree
                x1h, y1h, x2h, y2h = house

                box_shape_1 = [[x1t, y1t], [x2t, y1t], [x2t, y2t], [x1t, y2t]]
                box_shape_2 = [[x1h, y1h], [x2h, y1h], [x2h, y2h], [x1h, y2h]]
                polygon_1 = Polygon(box_shape_1)
                polygon_2 = Polygon(box_shape_2)
                intersect = polygon_1.intersection(polygon_2).area / polygon_1.union(polygon_2).area
                if intersect > minOverlap:
                    cleaning = True
                if intersect > maxOverlap:
                    maxOverlap = intersect

        print("Cleaning?:", cleaning, f'\nMax overlap: {round(maxOverlap*100, 2)}%')
        # show_result_pyplot(model, img, result, score_thr=0.6)
        # model.show_result(img, result, out_file=f'{args.dir}/random/result{args.name}')

    else:
        testImgs = os.listdir(f'data/{subdir}/test')
        for i in range(args.count):
            # test a single image and show the results
            randImg = random.choice(testImgs)
            img = f'data/{subdir}/test/{randImg}'  # or img = mmcv.imread(img), which will only load it once
            result = inference_detector(model, img)
            if args.count==1:
                # visualize the results in a new window
                show_result_pyplot(model, img, result, score_thr=0.6)# show the image with result
            # or save the visualization results to image files
            model.show_result(img, result, out_file=f'{args.dir}/result{randImg}')