''' Copyright FERAMS : 2020 '''

# Importing Packages
import os
import cv2
import numpy as np
from PIL import Image
import shutil
from SQLite import InitialiseDatabase


#  Getting ID from student's captured faces
def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
    return np.array(IDs), faces


# Training dataset of student's details with their recognised faces and their IDs and saving it into YML file
def TrainDataset():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataset/'
    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')

    Ids = []
    Faces = []
    for folder in os.listdir(path):
        Id, face = getImagesWithID(path+folder+'/')
        for i in Id:
            Ids.append(i)
        for j in face:
            Faces.append(j)
    recognizer.train(Faces, np.array(Ids))
    recognizer.save('recognizer/trainingData.yml')


# Initialising our dataset if dataset is empty
def EmptyTrain():
    path = 'recognizer'
    try:
        shutil.rmtree(path)
        InitialiseDatabase()
    except Exception as e:
        print(str(e))