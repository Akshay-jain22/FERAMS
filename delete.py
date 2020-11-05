''' Copyright FERAMS : 2020 '''

# Importing Packages
import os
import shutil
from train import TrainDataset, EmptyTrain
import csv


def DeleteStudent(roll_no):
    path = 'dataset/'
    flag = False
    find_roll_no = []
    folders = os.listdir(path)
    no_of_folders = len(folders)

    # Getting Dataset folder name using Roll Number
    for folder in folders:
        name = str(folder)
        y = name.split('-')
        if y[0] == roll_no:
            folder_name = folder
            flag = True
        
    if flag == False:
        return "Student does not exist"

    # Removing details from register file
    with open('register.csv', 'r') as file:
        lines = file.readlines()
    with open('register.csv', 'w') as new_file:
        for line in lines:
            entry = line.split(',')
            if entry[1] != roll_no:
                new_file.writelines(line)

    if os.path.exists(path+folder_name):
        try:
            # Removing student folder from dataset
            path1 = os.path.join(path, folder_name)
            shutil.rmtree(path1)
            no_of_folders = no_of_folders - 1

            # condition for Empty Dataset Folder
            if no_of_folders != 0:
                TrainDataset()
            else:
                EmptyTrain()
            return "Student Data Removed Successfully"

        except OSError as error:
            return "Error in Removing Student Data"
