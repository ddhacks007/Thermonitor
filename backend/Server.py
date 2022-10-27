from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import base64
import json
import os
from tools.GlassSegmenter import Evaluator
import time 
from WPS.test import test

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@cross_origin
@app.route('/upload', methods = ['POST'])
def upload_file():
   
   if request.method == 'POST':
      f = request.files['file']
      input_dir = 'inputs'
      os.makedirs(input_dir, exist_ok=True)
      file_name = secure_filename(f.filename)
      file_path = os.path.join(input_dir, file_name)
      f.save(file_path)
      print(os.listdir('./inputs'))
      time.sleep(4)
      print(file_path, file_name, ' saved .. ')
    #   time.sleep(5)
      eval = Evaluator()
      binary_image = eval.eval(file_name)
      print(binary_image)
      final_image_path = test(file_path, binary_image)

      with open(final_image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
      
      return json.dumps({'data': 'data:image/jpeg;base64,'+encoded_string.decode()}, default=str), 200

@cross_origin
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'
      

if __name__ == "__main__":

    app.run(debug=False)