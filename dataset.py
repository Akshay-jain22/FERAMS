''' Copyright FERAMS : 2020 '''

# Importing Packages
import cv2
import sqlite3
import os
import mtcnn
import csv
from train import TrainDataset
from datetime import date


# Saving student's details into csv file
def register(name, roll_no, branch):
    filename = 'register.csv'
    with open(filename, 'r+') as csv_file:
        myDataList = csv_file.readlines()
        roll_no_List = []
        for line in myDataList[1:]:
            entry = line.split(',')
            roll_no_List.append(entry[1])
        if roll_no not in roll_no_List:
            csv_file.writelines(f'{name},{roll_no},{branch}\n')

    today_date = date.today()  # YYYY : MM : DD
    filename = f'attendance/attendance - ' + str(today_date) + '.csv'

    if os.path.isfile(filename):
        with open(filename, 'r+') as csv_file:
            csv_file.writelines(f'{name},{roll_no},{branch},0,0,0,0,0,\n')


def Entry(uname, your_roll_no, branch):
    # Connecting database
    conn = sqlite3.connect('database.db')
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    c = conn.cursor()

    face_detector = mtcnn.MTCNN()
    cap = cv2.VideoCapture(0)
    new_folder = str(your_roll_no) + "-" + str(uname) + "-" + str(branch)
    if not os.path.exists("dataset/" + new_folder):
        os.mkdir("dataset/" + new_folder)
    else:
        return "Student already exists!!!"

    c.execute('INSERT INTO users (roll_no) VALUES (?)', (your_roll_no,))
    uid = c.lastrowid
    sampleNum = 0

    while True:
        ret, img = cap.read()

        # Detecting faces from live Camera and cropping the faces
        faces = face_detector.detect_faces(img)
        for res in faces:
            x, y, w, h = res['box']
            x, y = abs(x), abs(y)
            x1, y1 = x+w, y+h
            sampleNum = sampleNum+1
            image = img[y:y1, x:x1]
            image = cv2.resize(image, (256, 320))

            # Saving the cropped faces with ID
            cv2.imwrite("dataset/" + new_folder + "/Student." +
                        str(uid) + "." + str(sampleNum) + ".jpg", image)
            register(uname, your_roll_no, branch)
            cv2.rectangle(img, (x, y), (x1, y1), (255, 0, 0), 2)
            cv2.waitKey(20)
        cv2.waitKey(1)
        if sampleNum >= 15:
            break

    cap.release()
    conn.commit()
    conn.close()
    cv2.destroyAllWindows()

    # Training the Dataset
    TrainDataset()

    return "Student Data Registered!!!"
