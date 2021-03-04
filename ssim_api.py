import flask
from flask import request, jsonify

from skimage.metrics import structural_similarity as ssim
import cv2
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def load_images_from_folder(folder):
    # filename = os.listdir(folder)
    filename = []
    for img in os.listdir(folder):
        if img.endswith("jpg"):
            filename.append(img)

    return filename

def img_comparison(input1, input2):

    imageA = cv2.imread(input1)
    dimensions = imageA.shape

    if dimensions[0]>dimensions[1]:
        imageA = cv2.rotate(imageA, cv2.cv2.ROTATE_90_CLOCKWISE)
        dimensions = imageA.shape

    while dimensions[1]>1000 or dimensions[0]>1000: 
        scale_percent = 25 # percent of original size
        width = int(dimensions[1] * scale_percent / 100)
        height = int(dimensions[0] * scale_percent / 100)
        dim = (width, height)
        imageA = cv2.resize(imageA, dim, interpolation = cv2.INTER_AREA)
        dimensions = imageA.shape

    imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    
    dim = (dimensions[1],dimensions[0])

    # imageA = cv2.resize(imageA, dim, interpolation = cv2.INTER_AREA)

    images = load_images_from_folder(input2)

    imageB = []
    for image in images:
        img = cv2.imread(input2 + '\\' + image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dimensions = img.shape
        if dimensions[0]>dimensions[1]:
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
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

app.run(host='0.0.0.0')
