import os
import cv2
import face_recognition

def recog(frame):
    # input frame
    # Create arrays of known face encodings and their names
    known_face_encodings = []
    known_face_names = []
    for f_name in os.listdir('./known_people'):
        try:
            img = face_recognition.load_image_file('{}/{}'.format(
                './known_people', f_name))
            enc = face_recognition.face_encodings(img)[0]
            known_face_encodings.append(enc)
            known_face_names.append(f_name[:f_name.find('.')])
            print('[INFO] face recognizer for {} success...'.format(f_name))
        except:
            print('[INFO] face recognizer for {} fail...'.format(f_name))

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings,
                                                    face_encoding)
        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)
    return face_locations, face_names

#return face_locations + face_names