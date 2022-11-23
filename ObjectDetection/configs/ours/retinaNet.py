import os
_base_ = '../retinanet/retinanet_r50_fpn_1x_coco.py'

model = dict(
    bbox_head = dict(
        num_classes=2
    )
)

dataset_type = 'COCODataset'
classes = ('tree','house')

subdir = '1027data' #change accordingly
data = dict(
    samples_per_gpu=6,
    workers_per_gpu=2,
    train=dict(
        img_prefix=f'data/{subdir}/train/',
        classes=classes,
        ann_file=f'data/{subdir}/annotations/ember_train_dataset.json'),
    val=dict(
        img_prefix=f'data/{subdir}/val/',
        classes=classes,
        ann_file=f'data/{subdir}/annotations/ember_val_dataset.json'),
    test=dict(
        img_prefix=f'data/{subdir}/test/',
        classes=classes,
        ann_file=f'data/{subdir}/annotations/ember_test_dataset.json')
)


runner = dict(type='EpochBasedRunner', max_epochs=12)
evaluation = dict(interval=4, metric='bbox')
optimizer = dict(type='SGD', lr=0.0025, momentum=0.9, weight_decay=0.0001)

checkpoint_config = dict(interval=12)

load_from = 'checkpoints/retinanet_r50_fpn_1x_coco_20200130-c2398f9e.pth'
experiment = 'exp2_R' #change accordingly
if not os.path.exists(f'./exps/{experiment}'):
    os.mkdir(f'./exps/{experiment}')
work_dir = f'./exps/{experiment}'
gpu_ids = [1]