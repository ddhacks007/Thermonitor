import glob
import os
from PIL import Image
import numpy as np
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader

class ImageDataset(Dataset):
    def __init__(self, root, transforms_=None, unaligned=False, mode='train'):
        self.transform = transforms.Compose(transforms_)
        self.unaligned = unaligned
        self.mode = mode
        if self.mode == 'train':
            self.files_A = sorted(glob.glob(os.path.join(root+'/train/*/*')))
            self.files_B = sorted(glob.glob(os.path.join(root+'/train/*/*')))
        elif self.mode == 'test':
            self.files_A = sorted(glob.glob(os.path.join(root+'/test/*/*')))[:250]
            self.files_B = sorted(glob.glob(os.path.join(root+'/test/*/*')))[:250]
    def  __getitem__(self, index):
        image_A = Image.open(self.files_A[index % len(self.files_A)]+'/rgb.png')
        image_B = np.load(self.files_B[index % len(self.files_B)]+'/temperature.npy')
        image_B = (image_B - np.min(image_B)) / (np.max(image_B) - np.min(image_B)) * 255
        image_B = Image.fromarray(image_B).convert('RGB')
        item_A = self.transform(image_A)
        item_B = self.transform(image_B)
        return {'A':item_A, 'B':item_B}
    
    def __len__(self):
        return max(len(self.files_A), len(self.files_B))