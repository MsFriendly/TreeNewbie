from cgi import test

from cv2 import threshold
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import matplotlib.pyplot as plt
import argparse
import os
import random
import cv2
import json
import torch
import time

device = "cuda:0" if torch.cuda.is_available() else "cpu"

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=1, help="how many times to do inference")
parser.add_argument("--dir", type=str, default="visualResults", help="folder to save visual results")
parser.add_argument("--name", type=str, default="", help="specific image u want to test (put in data/random/test) [count=1]")
parser.add_argument("--type", type=str, default="img", help="type of inference (img / video)")
args = parser.parse_args()

# CHANGE THESE PARAMETERS AS NEEDED
# - Specify the path to model config and checkpoint file
config_file = 'configs/ours/modelConfig.py'
checkpoint_file = 'exps/exp3_F/epoch_24.pth'
# - Data sub-directory name
subdir = '1027data'
# - If tesing with video
videoF = "video1.mp4"
saveName = f'{subdir}videoResult1' #filename for video result
# - Threshold
thred = 0.5 #show predict bbox with probability above this

if not os.path.exists(os.getcwd()+"/"+args.dir):
    os.mkdir(os.getcwd()+"/"+args.dir)

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device=device)

if args.type == "img":
    if args.name != "":
        img = f'data/random/test/{args.name}'
        result = inference_detector(model, img)
        show_result_pyplot(model, img, result, score_thr=0.6)
        model.show_result(img, result, out_file=f'{args.dir}/random/result{args.name}')

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

            # draw ground-truth
            # image = cv2.imread(f'{args.dir}/result{randImg}')
            # with open(f'data/{subdir}/annotations/ember_test_dataset.json','r') as j:
            #     annt = json.load(j)
            # for ann in annt['annotations']:
            #     if ann['image_id'] == int(randImg[:-4]):
            #         x_top_left, y_top_left, bbx_width, bbx_height = ann['bbox']
            #         x_center = bbx_width/2 + x_top_left
            #         y_center = bbx_height/2 + y_top_left
            #         x_bottom_right = int(x_center + bbx_width/2)
            #         y_bottom_right = int(y_center + bbx_height/2)
            #         draw_bbox = cv2.rectangle(image,(x_top_left,y_top_left),(x_bottom_right, y_bottom_right),(255,255,0),1)
            #         # print(f'{args.dir}/result_gt{randImg}')
            #         cv2.imwrite(f'{args.dir}/result_gt{randImg}', draw_bbox)
elif args.type == "video":
    # test a video and show the results
    video = mmcv.VideoReader(f'data/{subdir}/{videoF}')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{args.dir}/{saveName}.mp4', fourcc, video.fps, (video.width, video.height))

    frame_count = 0 # To count total frames.
    total_fps = 0 # To get the final frames per second.

    for frame in mmcv.track_iter_progress(video):
        # Increment frame count.
        frame_count += 1
        start_time = time.time()# Forward pass start time.
        result = inference_detector(model, frame)
        end_time = time.time() # Forward pass end time.
        # Get the fps.
        fps = 1 / (end_time - start_time)
        # Add fps to total fps.
        total_fps += fps
        show_result = model.show_result(frame, result, score_thr=thred)
        # Write the FPS on the current frame.
        cv2.putText(
            show_result, f"{fps:.3f} FPS", (15, 30), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 0, 255), 2, cv2.LINE_AA
        )
        mmcv.imshow(show_result, 'Result', wait_time=1)
        out.write(show_result)
    # Release VideoCapture()
    out.release()
    # Close all frames and video windows
    cv2.destroyAllWindows()
    # Calculate and print the average FPS
    avg_fps = total_fps / frame_count
    print(f"Average FPS: {avg_fps:.3f}")