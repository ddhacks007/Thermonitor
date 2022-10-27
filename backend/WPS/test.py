import os
from tqdm.notebook import tqdm

import numpy as np
import torchvision.transforms as transforms
from torchvision.transforms import InterpolationMode
import torch
from PIL import Image

from WPS.models import GeneratorResNet 
import cv2

def test(image_path, mask):
    img_height = 256
    img_width = 256
    channels = 3
    input_shape = (channels, img_height, img_width) # (3,256,256)
    n_residual_blocks = 9 # suggested default, number of residual blocks in generator
    G_AB = GeneratorResNet(input_shape, n_residual_blocks)
    transforms_test = [
        transforms.Resize((int(img_height),int(img_height)), InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ]
    model = torch.load("./WPS/checkpoints/model.pt", map_location=torch.device('cpu'))
    G_AB.load_state_dict(model['generator_state_dict_AB'])
    print("Checkpoint Loaded..")
    G_AB.eval()
    transforms_ = transforms.Compose(transforms_test)
    cuda = torch.cuda.is_available()
    if cuda:
        G_AB.cuda()
    Tensor = torch.cuda.FloatTensor if cuda else torch.Tensor
    img = Image.fromarray(cv2.imread(image_path)[:, :, ::-1])
    img_org = cv2.resize(np.array(img).copy(), (256, 256),  interpolation=cv2.INTER_NEAREST).astype(np.uint8)
    img = transforms_(img)
    img = img.unsqueeze(0)
    img = img.type(Tensor)
    img_g = G_AB(img)
    print("Creating Images..")
    # Get the generated image and process it 
    img_g = img_g[0].detach().cpu().numpy().transpose(1, 2, 0)
    img_g = (img_g - np.min(img_g)) / (np.max(img_g) - np.min(img_g))*255.
    img_rgb = img_g.copy()
    
    # Blur the image (for denoising) and threshold it
    img_g = cv2.cvtColor(img_g, cv2.COLOR_BGR2GRAY)
    img_g = np.uint8(img_g)
    img_g = cv2.GaussianBlur(img_g, (3, 3), 0)
    (T, threshInv) = cv2.threshold(img_g, 0, 255,
                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                                  
    # Fill the small holes and threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    img_g = cv2.morphologyEx(img_g,cv2.MORPH_OPEN,kernel)
    img_bef_th = img_g.copy()
    (T, img_g) = cv2.threshold(img_g, 170, 255, cv2.THRESH_BINARY)
    print(img_g.shape, mask.shape)

    # Apply the window segmented maska dn find the contours to draw
    img_g = cv2.bitwise_and(img_g,img_g,mask = mask)
    contours, hierarchy = cv2.findContours(img_g, 
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img_rgb, contours, -1, (0, 255, 0), 3)  
    
    # Convert all the outputs to BGR for consistency
    img_bef_th = cv2.cvtColor(img_bef_th, cv2.COLOR_GRAY2BGR)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    vis = np.concatenate((img_org, mask, img_rgb), axis=0)
    
    if not os.path.exists("web_result"):
        os.mkdir("web_result")
    path = "web_result/result.jpg"
    cv2.imwrite(path, vis)
    return path

#test('test/test2.jpeg', np.random.randint(2, size=(256,256), dtype=np.uint8))
	