from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import imutils
from imutils import contours
import os
import flask
from datetime import datetime

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app_root = os.path.dirname(os.path.abspath(__file__))

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['POST'])
def process_image():
    data = {}
    data["area"] = []
    data["input"] = []
    data["gray"] = []
    data["output"] = []
    now = datetime.now()

    input = os.path.join(app_root, 'static/input')
    grayscale = os.path.join(app_root, 'static/grayscale')
    output = os.path.join(app_root, 'static/output')

    file = request.files['image']
    filter_size = request.form['filter_size']
    sigma_color = request.form['sigma_color']
    sigma_space = request.form['sigma_space']
    min_value = request.form['min_value']
    max_value = request.form['max_value']

    file_name = file.filename or ''
    file_name_time = str(datetime.timestamp(now))+file_name

    input_dest = '/'.join([input, file_name_time])
    grayscale_dest = '/'.join([grayscale, file_name_time])
    output_dest = '/'.join([output, file_name_time])

    file.save(input_dest)

    input_img = cv2.imread(input_dest, cv2.IMREAD_UNCHANGED)

    scale_percent = 20
    width = int(input_img.shape[1] * scale_percent / 100)
    height = int(input_img.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(input_img, dim, interpolation = cv2.INTER_AREA)

    cv2.imwrite(input_dest, image)

    input_path = flask.url_for('static', filename='input/'+file_name_time)
    data["input"].append('http://localhost:5000'+input_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, int(filter_size), int(sigma_color), int(sigma_space))

    ret, _ = cv2.threshold(gray, thresh=0, maxval=255, type=(cv2.THRESH_BINARY + cv2.THRESH_OTSU))

    edged = cv2.Canny(gray, threshold1=ret*float(min_value), threshold2=ret*float(max_value),
     apertureSize=3, L2gradient=True)

    cv2.imwrite(grayscale_dest, edged)

    grayscale_path = flask.url_for('static', filename='grayscale/'+file_name_time)
    data["gray"].append('http://localhost:5000'+grayscale_path) 

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)

    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))

    for (i, c) in enumerate(cnts):
        print("Area #{}:".format(i + 1))
        area = cv2.contourArea(c)
        print(area)
        area_nm = area * 0.21

        (x,y),radius = cv2.minEnclosingCircle(c)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(image,center,radius,(0,255,0),1)
        data["area"].append({"location": (int(5*x),int(5*y)), "size": round(area_nm, 2)})

        cv2.putText(image, "#{}".format(i + 1),
            (int(x), int(y)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

    cv2.imwrite(output_dest, image)

    output_path = flask.url_for('static', filename='output/'+file_name_time)
    data["output"].append('http://localhost:5000'+output_path)

    return jsonify(data)


if __name__ == '__main__':
    app.run()