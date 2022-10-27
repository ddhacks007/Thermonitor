# Thermonitor UI
go into the theromitor-ui module and run the command
- ```npm install ```
- ```npm start```


# Thermonitor Backend
DATASETS USED:
- Trans10K
- RGBT


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
[Google Drive](https://drive.google.com/file/d/1dsNOWfvsDzKlmsWxgWVCwh0j84zKnof6/view?usp=sharing)
Add the checkpoint into the checkpoint directory present in the WPS directory present in the backend module of this project.

## Turn ON the FLASK server present in the backend-module
  ```python3 Server.py ```


```

You can route to the upload page of our web app, upload and view the results of our model.
