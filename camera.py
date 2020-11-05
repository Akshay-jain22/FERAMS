''' Copyright FERAMS : 2020 '''

# Importing Packages
import cv2
import numpy as np
import sqlite3
import os
import mtcnn
import csv
from datetime import date, datetime
from model import FacialExpressionModel
import json


# Creating CSV File for attendance details
def CreateCSV(filename):
    with open('register.csv', 'r') as file:
        lines = file.readlines()
    with open(filename, 'w') as new_file:
        new_file.writelines(
            'NAME,ROLL NUMBER,BRANCH,ANGRY,HAPPY,NEUTRAL,SAD,SURPRISE,ATTENDANCE TIME\n')
        for line in lines[1:]:
            new_line = line[:-1] + ',0,0,0,0,0,\n'
            new_file.writelines(new_line)


def Attendance(roll_no):
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    today_date = date.today()  # YYYY : MM : DD
    filename = f'attendance/attendance - ' + str(today_date) + '.csv'

    # Copying the data of file in List
    with open(filename, 'r+') as csv_file:
        List = csv_file.readlines()

    # Marking attendance of roll_no
    with open(filename, 'w') as csv_file:
        for line in List:
            entry = line.split(',')
            if(entry[1] == roll_no and entry[8] == "\n"):
                line = line[:-1] + time + '\n'
            csv_file.writelines(str(line))


# Returns whether Attendance should be marked or not
def count(roll_no, pred):
    now = datetime.now()
    today_date = date.today()  # YYYY : MM : DD
    filename = f'attendance/attendance - ' + str(today_date) + '.csv'
    Expression_Count = 0

    # Getting Column for provided expression
    if(pred == "Angry"):
        index = 3
    elif (pred == "Happy"):
        index = 4
    elif (pred == "Neutral"):
        index = 5
    elif (pred == "Sad"):
        index = 6
    elif (pred == "Surprise"):
        index = 7
    else:
        return False

    # Create Attendance CSV File if not exists
    if not os.path.isfile(filename):
        CreateCSV(filename)

    with open(filename, 'r') as csv_file:
        List = csv_file.readlines()

    # Marking it's predicted expression in attendance file
    with open(filename, 'w') as csv_file:
        for line in List:
            entry = line.split(',')
            if(entry[1] == roll_no):
                entry[index] = "1"
                line = entry[0]
                for i in range(1, len(entry)):
                    if i == index:
                        line = line + ',' + entry[index]
                    else:
                        line = line + ',' + entry[i]

                # Calculating the count for that roll_no
                Expression_Count = sum([int(entry[i]) for i in range(3, 8)])

            csv_file.writelines(line)

        if(Expression_Count >= 2):
            return True
        else:
            return False


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0) # 0 - Default WebCam, 1 - External Camera , path - Path_To_Video

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions and names
    def get_frame(self):

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        fname = "recognizer/trainingData.yml"
        if not os.path.isfile(fname):
            print("\nPlease train the data first\n")
            return None

        # Model For Facial Expression Recognition
        model = FacialExpressionModel("model.json", "model_weights.h5")

        # Model For Face Recognizer
        face_detector = mtcnn.MTCNN()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(fname)

        _, img = self.video.read()
        faces = face_detector.detect_faces(img)

        for res in faces:
            x, y, w, h = res["box"]
            x, y = abs(x), abs(y)
            x1, y1 = x+w, y+h
            image = img[y:y1, x:x1]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Recognizing Face
            ids, conf = recognizer.predict(image)
            c.execute("select roll_no from users where id = (?);", (ids,))
            result = c.fetchall()
            try:
                roll_no = result[0][0]
            except:
                roll_no = 'Error'

            if conf > 50:
                roll_no = "No Match"

            image2 = cv2.resize(image, (48, 48))

            # Predicting Expression
            pred = model.predict_emotion(image2[np.newaxis, :, :, np.newaxis])

            msg = pred + " " + roll_no

            # Mark the Expression if Face is detected
            if roll_no != "Error" and roll_no != "No Match" :
                marked = count(roll_no, pred)
                if(marked):
                    Attendance(roll_no)
                    msg = "MARKED"

            cv2.putText(img, msg, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 0), 2)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
