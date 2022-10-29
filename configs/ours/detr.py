import os
_base_ = '../detr/detr_r50_8x2_150e_coco.py'

model = dict(
    bbox_head = dict(
        num_classes=1
    )
)

dataset_type = 'COCODataset'
classes = ('ember',)

subdir = '0425take3' #change accordingly
data = dict(
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
        ann_file=f'data/{subdir}/annotations/ember_test_dataset.json'))


runner = dict(type='EpochBasedRunner', max_epochs=800) #default: 12
evaluation = dict(interval=10, metric='bbox')
# optimizer = dict(type='SGD', lr=0.0025, momentum=0.9, weight_decay=0.0001)

checkpoint_config = dict(interval=50) #, by_epoch=False

load_from = 'checkpoints/detr_r50_8x2_150e_coco_20201130_194835-2c4b8974.pth'
# resume_from = 'exps/0721_exp11/latest.pth'
experiment = 'testrun' #change accordingly
if not os.path.exists(f'./exps/{experiment}'):
    os.mkdir(f'./exps/{experiment}')
work_dir = f'./exps/{experiment}'
gpu_ids = [1]