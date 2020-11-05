''' Copyright FERAMS : 2020 '''

''' Main File for Flask Web-App of FERAMS '''

# Importing Packages
from flask import Flask, render_template, Response, request, url_for, jsonify
from camera import VideoCamera, CreateCSV
from delete import DeleteStudent
from datetime import date, datetime
from dataset import Entry
import os
import json

# Initialising Flask WebApp
app = Flask(__name__)


# Root Template
@app.route('/')
def index():
    return render_template('index.html')


# Template for Marking Attendance
@app.route('/mark_attendance')
def mark_attendance():
    return render_template('mark_attendance.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Template for User Authentication
@app.route('/authentication', methods=['POST', 'GET'])
def authentication():
    if request.method == 'POST':
        val = request.form.get('choice')
        with open('config.json', 'w') as file:
            json.dump({"choice" : val}, file)
        return render_template('auth.html', val=val)

    else :
        with open('config.json', 'r') as file:
            val = json.load(file)['choice']
        return render_template('auth.html', val=val)


# Template for Student Registration
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dataset')
def dataset():
    try:
        uname = request.args.get('name', type=str)
        your_roll_no = request.args.get('rollno', type=str)
        branch = request.args.get('branch', type=str)

        result = Entry(uname, your_roll_no, branch)
        return jsonify(result=result)
    except Exception as e:
        return str(e)


# Template for Deleting Student Data
@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/deleteStudent')
def deleteStudent():
    try:
        roll_no = request.args.get('rollno', type=str)

        result = DeleteStudent(roll_no)
        return jsonify(result=result)
    except Exception as e:
        return str(e)


# Template for displaying Student List
@app.route('/list')
def student_list():
    lists = attendance_list()
    return render_template('student_list.html', lists=lists)

def attendance_list():
    now = datetime.now()
    today_date = date.today()  # YYYY : MM : DD
    filename = f'attendance/attendance - ' + str(today_date) + '.csv'

    # Create Attendance CSV File if not exists
    if not os.path.isfile(filename):
        CreateCSV(filename)

    with open(filename, 'r') as csv_file:
        List = csv_file.readlines()
    return List


'''
# Run Flask WebApp on LocalHost
# LocalHost Server : http://127.0.0.1:5000/
# To TurnOff the localhost : Ctrl + C
'''
if __name__ == '__main__':
    app.run(debug=True)
