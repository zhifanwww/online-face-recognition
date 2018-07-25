# import needed packages
from flask import Flask, request, send_file, send_from_directory, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import base64
import re
import numpy as np
from skimage.io import imread
from skimage.color import rgba2rgb
from io import BytesIO
import new_recog
from skimage import img_as_ubyte
import boto3

app = Flask(__name__)


# when requesting the URL '/', return index.html
@app.route('/')
def index():
    return send_file("index.html")

# indicate the location of required css
@app.route('/css/<path:path>')
def css(path):
    return send_from_directory("css", path)

# indicate the location of required js
@app.route('/js/<path:path>')
def js(path):
    return send_from_directory("js", path)

# when the form element requests the URL '/image', save the uploaded image to the filefolder 'known_people' 
# and redirect to the index page
@app.route('/image', methods=["POST"])
def uploadImage():
    myfile = request.files['people']
    myfile.save('known_people/' + secure_filename(myfile.filename))
    return redirect(url_for('index'))

# dealing with face recognition
# this funtion accepts a frame in format of base64 and invokes funtions in 'new_recog.py' to do a face recognition after parsing it. 
@app.route('/stream', methods=["PUT"])
def streaming():
    data = request.data
    length = len("data:image/png;base64,")
    data = data[length:] # remove the header of base64
    pngframe = base64.decodebytes(data)
    frame = imread(BytesIO(pngframe)) # in format of (150, 300, 4)
    frame = rgba2rgb(frame)
    frame = img_as_ubyte(frame)
    frame = frame.astype(np.uint8)

    # get face_locations, face_names from calling the face_recognition library
    face_locations, face_names = new_recog.recog(frame)

    # when exceeding the warning_count, send a warning
    for name in face_names:
        # record the unknown counts in file count.txt
        if name == "Unknown":
            with open('count.txt', 'r+') as c:
                count = int(c.read())
                count += 1
                if count >= 20:
                    count = 0
                    warning()
                c.seek(0)
                c.truncate()
                c.write(str(count))
                c.close()
            break
    return jsonify(locations=face_locations, names=face_names)

def warning():
    # set up a client
    client = boto3.client(
        "sns",
        region_name="us-east-2"
    )

    # Send the sms message
    client.publish(
        Message="Hey, this is a warning message! Someone unknown is in the surveillance",
        TargetArn=" "#targetArn
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
