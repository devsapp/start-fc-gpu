optimizer = dict(type='SGD', lr=0.02, momentum=0.9, weight_decay=0.0005)
optimizer_config = dict(grad_clip=None)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=1500,
    warmup_ratio=0.001,
    step=[440, 544])
total_epochs = 640
checkpoint_config = dict(interval=80)
log_config = dict(interval=100, hooks=[dict(type='TextLoggerHook')])
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
dataset_type = 'RetinaFaceDataset'
data_root = '/data/vdb/yuxiang.tyx/FaceDet/WiderFace/'
train_root = data_root + 'WIDER_train/'
val_root = data_root + 'WIDER_val/'
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=3,
    train=dict(
        type='RetinaFaceDataset',
        ann_file=train_root+'labelv2.txt',
        img_prefix=train_root+'images/',
        pipeline=[
            dict(type='LoadImageFromFile', to_float32=True),
            dict(type='LoadAnnotationsV2', with_bbox=True, with_keypoints=True),
            dict(
                type='RandomSquareCrop',
                crop_choice=[0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                big_face_ratio=0.2,
                big_face_crop_choice=[0.65, 0.7, 0.8, 0.9, 0.95],
                bbox_clip_border=False),
            dict(type='RotateV2', level=5, prob=0.3, max_rotate_angle=180, random_negative_prob=0.5),
            dict(type='RotateV2', level=5, prob=0.3, max_rotate_angle=360, random_negative_prob=0.5),
            dict(
                type='ResizeV2',
                img_scale=(640, 640),
                keep_ratio=False,
                bbox_clip_border=False),
            dict(type='RandomFlipV2', flip_ratio=0.5),
            dict(
                type='PhotoMetricDistortion',
                brightness_delta=32,
                contrast_range=(0.5, 1.5),
                saturation_range=(0.5, 1.5),
                hue_delta=18),
            dict(
                type='Normalize',
                mean=[127.5, 127.5, 127.5],
                std=[128.0, 128.0, 128.0],
                to_rgb=True),
            dict(type='DefaultFormatBundleV2'),
            dict(
                type='Collect',
                keys=[
                    'img', 'gt_bboxes', 'gt_labels', 'gt_bboxes_ignore',
                    'gt_keypointss'
                ])
        ]),
    val=dict(
        type='RetinaFaceDataset',
        ann_file=val_root+'labelv2.txt',
        img_prefix=val_root+'images/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(640, 640),
                flip=False,
                transforms=[
                    dict(type='ResizeV2', keep_ratio=True),
                    dict(type='RandomFlipV2', flip_ratio=0.0),
                    dict(
                        type='Normalize',
                        mean=[127.5, 127.5, 127.5],
                        std=[128.0, 128.0, 128.0],
                        to_rgb=True),
                    dict(type='Pad', size=(640, 640), pad_val=0),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ]),
    test=dict(
        type='RetinaFaceDataset',
        ann_file=val_root+'labelv2.txt',
        img_prefix=val_root+'images/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(640, 640),
                flip=False,
                transforms=[
                    dict(type='ResizeV2', keep_ratio=True),
                    dict(type='RandomFlipV2', flip_ratio=0.0),
                    dict(
                        type='Normalize',
                        mean=[127.5, 127.5, 127.5],
                        std=[128.0, 128.0, 128.0],
                        to_rgb=True),
                    dict(type='Pad', size=(640, 640), pad_val=0),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ]))
model = dict(
    type='SCRFD',
    backbone=dict(
        type='ResNetV1e',
        depth=0,
        block_cfg=dict(
            block='Bottleneck',
            stage_blocks=(17, 16, 2, 8),
            stage_planes=[56, 56, 144, 184]),
        base_channels=56,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=False,
        style='pytorch'),
    neck=dict(
        type='PAFPN',
        in_channels=[224, 224, 576, 736],
        out_channels=128,
        start_level=1,
        add_extra_convs='on_output',
        num_outs=3),
    bbox_head=dict(
        type='SCRFDHead',
        num_classes=1,
        in_channels=128,
        stacked_convs=2,
        feat_channels=256,
        #norm_cfg=dict(type='BN', requires_grad=True),
        norm_cfg=dict(type='GN', num_groups=32, requires_grad=True),
        cls_reg_share=True,
        strides_share=True,
        scale_mode=2,
        anchor_generator=dict(
            type='AnchorGenerator',
            ratios=[1.0],
            scales=[1, 2],
            base_sizes=[16, 64, 256],
            strides=[8, 16, 32]),
        loss_cls=dict(
            type='QualityFocalLoss',
            use_sigmoid=True,
            beta=2.0,
            loss_weight=1.0),
        loss_dfl=False,
        reg_max=8,
        loss_bbox=dict(type='DIoULoss', loss_weight=2.0),
        use_kps=True,
        loss_kps=dict(
            type='SmoothL1Loss', beta=0.1111111111111111, loss_weight=0.2)  # kps loss_weight = 0.1 --> 0.2
        ),
    train_cfg=dict(
            assigner=dict(type='ATSSAssigner', topk=9),
            allowed_border=-1,
            pos_weight=-1,
            debug=False),
    test_cfg=dict(
        nms_pre=-1,
        min_bbox_size=0,
        score_thr=0.02,
        nms=dict(type='nms', iou_threshold=0.45),
        max_per_img=-1))
epoch_multi = 1
evaluation = dict(interval=80, metric='mAP')
