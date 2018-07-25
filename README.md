
Based on several blog posts on [pyimagesearch](https://www.pyimagesearch.com/).

Based on a simple face recognition library(https://github.com/ageitgey/face_recognition).

Based on Amazon's Messaging Service.

## Dependencies

- numpy
- opencv
- dlib
- imutils
- flask
- skimage
- base64
- re
- boto3

## How it works

1. Install all the dependencies.
2. Run the local server by `python app.py`. It will be by default running at locallost:8081.
3. In the opening webpage, upload the images of known people to the backend.
4. Set your Arn in the code.
5. Now, if there are any unknown people showing up over 20s in the video recorded by your webcam, an alarm email will be sent to the set email address.
