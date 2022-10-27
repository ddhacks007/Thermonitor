#Thermonitor UI
go into the theromitor-ui module and run the command
- npm install 
- npm start


# Thermonitor Backend
DATASETS USED:
1.) Trans10K
2.) RGBT


## Environments required for the backend of the thermonitor

- python 3
- torch = 1.1.0 (>1.1.0 with cause performance drop, we can't find the reason)
- torchvision
- pyyaml
- Pillow
- numpy
- flask
- flask-cors

## INSTALL
pretrained backbone models will be download automatically in pytorch default directory(```~/.cache/torch/checkpoints/```).

```
python setup.py develop
```
#This link contains the pre-trained model for the translab model which detects the transperancy in the image
[Google Drive](https://drive.google.com/drive/folders/1yJMEB4rNKIZt5IWL13Nn-YwckrvAPNuz?usp=sharing)
Add the checkpoint into the demo directory present inside the backed-module 

#This link contains the pre-trained model for the GAN model which generates the IR image from RGB IMAGE
[Google Drive]()
Add the checkpoint into the checkpoint directory present in the WPS directory present in the backend module of this project.

# Turn ON the FLASK server present in the backend-module
  python3 Server.py 


## Train
Our experiments are based on one machine with 8 V100 GPUs(32g memory), if you face memory error, you can try the 'batchsize=4' version.
### Train with batchsize=8(cost 15G memory)
```
bash tools/dist_train.sh configs/trans10K/translab.yaml 8 TRAIN.MODEL_SAVE_DIR workdirs/translab_bs8
```
### Train with batchsize=4(cost 8G memory)
```
bash tools/dist_train.sh configs/trans10K/translab_bs4.yaml 8 TRAIN.MODEL_SAVE_DIR workdirs/translab_bs4
```

You can route to the upload page of our web app, upload and view the results of our model.
