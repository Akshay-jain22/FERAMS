# FERAMS

`IT 204 Project : Nov 2020 : NITK`

FERAMS - Facial Expression Recognition and Attendance Management System

## Code
- #### [FERAMS Master Branch](https://github.com/Akshay-jain22/FERAMS/tree/master)

## Introduction
We have proposed an automated student attendance management system based on face recognition and facial expression recognition.
Along with Attendance Management, Our System also provides some other important functionalities:
1) Registration - The student who is not registered on system will also be able to register on the spot by seeking the administrative permission.
2) Deletion – The Administration can remove Student data which may be corrupted in some way.
3) Student List – The Administration can get the list of students marked as present along with the time.

` The average accuracy of Facial Expression Recognition is 66 percent and Face Recognition using MTCNN is 95 percent.`

## Key Contributions
- #### Face Recognition
1) Firstly, we detect the face of the person using MTCNN and then identify it using pre-trained model developed using our database.
2) Then we go for further steps for taking the attendance to avoid the proxy.

- #### Facial expression recognition
1) Once face recognition is done, we predict the expressions of the user and check whether the user expressions has changed at least once or not.
2) If the User expressions are changed, we continue the procedure.

- #### Marking The Attendance
1) Once above-mentioned procedures are completed successfully then marking of the attendance is done for the user. And we note down the time of entering the person and all details in a csv file that is saved in the system.
2) We can use this file for future references and the process continues for other users.

## Templates for Flask Web App–
```
a) Admin Dashboard
b) Attendance Manager
c) Admin Authentication
d) Student Registration
e) Student Deletion
f) Student List
```

## Advantages/Disadvantages
- #### Advantages of FERAMS
1) Easy installation in low Cost.
2) No Personal Data Breach.
3) Less chance of proxies.

- #### Disadvantages of FERAMS
1) Proxy using Videos

## Architecture Diagram
<img src="https://github.com/Akshay-jain22/FERAMS/blob/main/ARCHITECTURE%20DIAGRAM%20-%20FERAMS.png" width="800">

## Results and Analysis
- #### Web Application Snapshot
<img src="https://github.com/Akshay-jain22/FERAMS/blob/main/Flask%20WebApp.png" width="800">

- #### Confusion Matrix Analysis
<img src="https://github.com/Akshay-jain22/FERAMS/blob/main/Confusion%20Matrix%20-%20FERAMS.png" width="300">

- #### F1-Score
<img src="https://github.com/Akshay-jain22/FERAMS/blob/main/Analysis%20-%20FERAMS.png" width="300">

- #### Five-Point Scale Likert Analysis
<img src="https://github.com/Akshay-jain22/FERAMS/blob/main/Likert%20Analysis.png" width="500">

## References
- #### [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
- #### [CNN Tutorial](https://www.slideshare.net/Simplilearn/convolutional-neural-network-tutorial-cnn-how-cnn-works-deep-learning-tutorial-simplilearn)
- #### [Dataset for Facial Expression Recognition (FER2013)](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/)
- #### [MTCNN Documentation](https://pypi.org/project/mtcnn/)

## Developers
  - Akshay Jain
  - Ashok Kumar
  - Anand Kumar
  - Guru Aakash G
