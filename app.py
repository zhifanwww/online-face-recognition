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

# TRIM = re.compile("^data:image\/(png|jpg);base64,")

app = Flask(__name__)


@app.route('/')
def index():
    return send_file("index.html")


@app.route('/css/<path:path>')
def css(path):
    return send_from_directory("css", path)


@app.route('/js/<path:path>')
def js(path):
    return send_from_directory("js", path)

@app.route('/image', methods=["POST"])
def uploadImage():
    myfile = request.files['people']
    myfile.save('known_people/' + secure_filename(myfile.filename))
    return redirect(url_for('index'))

@app.route('/stream', methods=["PUT"])
def streaming():
    data = request.data
    length = len("data:image/png;base64,")
    #data = data.replace("data:image/png;base64,", "")
    data = data[length:]
    pngframe = base64.decodebytes(data)
    frame = imread(BytesIO(pngframe)) # (150, 300, 4)
    frame = rgba2rgb(frame)
    frame = img_as_ubyte(frame)
    frame = frame.astype(np.uint8)
    # with open("xxx.png", "wb") as f:
    #   f.write(pngframe)

    face_locations, face_names = new_recog.recog(frame)

    # when exceeding warning_count, send a warning
    for name in face_names:
        if name == "Unknown":
            with open('count.txt', 'r+') as c:
                count = int(c.read())
                count += 1
                if count >= 10:
                    count = 0
                    warning()
                c.seek(0)
                c.truncate()
                c.write(str(count))
                c.close()
            break
    return jsonify(locations=face_locations, names=face_names)

def warning():
    client = boto3.client(
        "sns",
        region_name="us-east-2"
    )

    # Send your sms message.
    client.publish(
        Message="Hey, this is a warning message! Someone unknown is in the surveillance",
        TargetArn="arn:aws:sns:us-east-2:426162095813:face_recog"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)