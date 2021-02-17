import flask
from flask import request, jsonify

from skimage.metrics import structural_similarity as ssim
import cv2
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def load_images_from_folder(folder):
    filename = os.listdir(folder)
    return filename

def img_comparison(input1, input2):

    imageA = cv2.imread(input1)
    imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)

    images = load_images_from_folder(input2)

    imageB = []
    for image in images:
        img = cv2.imread(input2 + '\\' + image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imageB.append(img)

    percent_ssim = []
    i = 0

    for image in imageB:
        s = ssim(imageA, image)
        dic  = {'similarity' : s, 'path' : images[i]}
        percent_ssim.append(dic)
        i = i + 1
    
    percent_ssim = sorted(percent_ssim, key = lambda i: i['similarity'],reverse=True)
    print(percent_ssim)
    return percent_ssim

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Image Similarity</h1>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/image_similarity', methods=['GET'])
def api_img_similarity():
    query_parameters = request.args

    input1 = query_parameters.get('input1')
    input2 = query_parameters.get('input2')

    if not (input1 and input2):
        return page_not_found(404)
    else:
        return jsonify(img_comparison(input1, input2))

app.run()