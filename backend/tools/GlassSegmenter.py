from __future__ import print_function

import os
import sys
import time
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import uuid
import logging
import torch
import torch.nn as nn
import torch.utils.data as data
import torch.nn.functional as F

from tabulate import tabulate
from torchvision import transforms
from segmentron.data.dataloader import get_segmentation_dataset
from segmentron.models.model_zoo import get_segmentation_model
from segmentron.utils.distributed import synchronize, make_data_sampler, make_batch_data_sampler
from segmentron.config import cfg
from segmentron.utils.options import parse_args
from segmentron.utils.default_setup import default_setup
from IPython import embed
from collections import OrderedDict
from segmentron.utils.filesystem import makedirs
import cv2
import numpy as np

cfg.update_from_file('configs/trans10K/translab.yaml')
cfg['TEST']['TEST_MODEL_PATH'] = 'demo/16.pth'
cfg.PHASE = 'test'
cfg.ROOT_PATH = root_path
cfg.DATASET.NAME = 'trans10k_extra'
cfg.check_and_freeze()

class Evaluator(object):
    def __init__(self):
        self.distributed = False
        self.device = torch.device("cpu")

        # image transform
        input_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(cfg.DATASET.MEAN, cfg.DATASET.STD),
        ])
        
        # dataset and dataloader
        val_dataset = get_segmentation_dataset(cfg.DATASET.NAME,
                                               root='./inputs',
                                               split='val',
                                               mode='val',
                                               transform=input_transform,
                                               base_size=cfg.TRAIN.BASE_SIZE)

        val_sampler = make_data_sampler(val_dataset, shuffle=False, distributed=self.distributed)
        val_batch_sampler = make_batch_data_sampler(val_sampler, images_per_batch=1, drop_last=False)

        self.val_loader = data.DataLoader(dataset=val_dataset,
                                          batch_sampler=val_batch_sampler,
                                          num_workers=cfg.DATASET.WORKERS,
                                          pin_memory=True)
        self.classes = val_dataset.classes
        # create network
        self.model = get_segmentation_model().to(self.device)

        if hasattr(self.model, 'encoder') and cfg.MODEL.BN_EPS_FOR_ENCODER:
                logging.info('set bn custom eps for bn in encoder: {}'.format(cfg.MODEL.BN_EPS_FOR_ENCODER))
                self.set_batch_norm_attr(self.model.encoder.named_modules(), 'eps', cfg.MODEL.BN_EPS_FOR_ENCODER)

        self.model.to(self.device)
        self.count_easy = 0
        self.count_hard = 0
    def set_batch_norm_attr(self, named_modules, attr, value):
        for m in named_modules:
            if isinstance(m[1], nn.BatchNorm2d) or isinstance(m[1], nn.SyncBatchNorm):
                setattr(m[1], attr, value)

    def eval(self, rec_filename):
        start = time.time()
        self.model.eval()
        if self.distributed:
            model = self.model.module
        else:
            model = self.model
        input_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(cfg.DATASET.MEAN, cfg.DATASET.STD),
        ])
        val_dataset = get_segmentation_dataset(cfg.DATASET.NAME,
                                               root='./inputs',
                                               split='val',
                                               mode='val',
                                               transform=input_transform,
                                               base_size=cfg.TRAIN.BASE_SIZE)

        val_sampler = make_data_sampler(val_dataset, shuffle=False, distributed=self.distributed)
        val_batch_sampler = make_batch_data_sampler(val_sampler, images_per_batch=1, drop_last=False)

        for i, (image, _, filename) in enumerate(self.val_loader):
            filename = filename[0]

            print(os.path.basename(filename), rec_filename)
            if os.path.basename(filename) == rec_filename:
                print('matched')
                image = image.to(self.device)
                makedirs('./results')
                save_path = os.path.join('results', f"{uuid.uuid1()}.png")

                with torch.no_grad():
                    output, output_boundary = model.evaluate(image)
                    ori_img = cv2.imread(filename)
                    h, w, _ = ori_img.shape

                    glass_res = output.argmax(1)[0].data.cpu().numpy().astype('uint8') * 127
                    glass_res = cv2.resize(glass_res, (256, 256), interpolation=cv2.INTER_NEAREST)
                    cv2.imwrite(save_path, glass_res)
                    print(glass_res.shape)
                    # os.remove(filename)
                    print(time.time() - start, ' seconds ')
                    print('deepak ... .. .. .. . ')
                    # self.val_loader = None

                    # quit()
                    return glass_res
