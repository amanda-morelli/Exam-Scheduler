#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:34:19 2020

EXAM SCHEDULER PROJECT
ESC190

AMANDA MORELLI
RIDAM LOOMBA
"""

import exam_scheduler
import tkinter as tk


exams = []
availability = []
day_times = []
scheduleMatrix = []
courseCode = ""


# GUI INITIALIZATION
root= tk.Tk()

canvas1 = tk.Canvas(root, width = 500, height = 500)
canvas1.pack()

header = tk.Label(root, text='UofT Engineering Exam Scheduler')
header.config(font=('helvetica', 20))
canvas1.create_window(250, 25, window=header)

coursecodelabel = tk.Label(root,text='course code: (ie ESC190H1)')
coursecodelabel.config(font=('helvetica', 12))
canvas1.create_window(110,80,window=coursecodelabel)

instructorlabel = tk.Label(root, text='instructor name:')
instructorlabel.config(font=('helvetica',12))
canvas1.create_window(390,80,window=instructorlabel)

durationlabel = tk.Label(root, text='duration of exam (hours):')
durationlabel.config(font=('helvetica',12))
canvas1.create_window(110, 130,window=durationlabel)

prioritylabel = tk.Label(root, text='priority of exam (1 = highest, 3 = lowest)')
prioritylabel.config(font=('helvetica',12))
canvas1.create_window(390, 130, window=prioritylabel)

classlabel = tk.Label(root, text='student class (23, 22, 21, 20):')
classlabel.config(font=('helvetica',12))
canvas1.create_window(110,180,window=classlabel)

locationlabel = tk.Label(root, text='location (OPTIONAL):')
classlabel.config(font=('helvetica',12))
canvas1.create_window(390,180,window=locationlabel)

date_timelabel = tk.Label(root, text='date & time (OPTIONAL):')
classlabel.config(font=('helvetica',12))
canvas1.create_window(110,230,window=date_timelabel)

# course_code
entry1 = tk.Entry (root) 
canvas1.create_window(110, 100, window=entry1)

# instructor
entry2 = tk.Entry(root)
canvas1.create_window(390, 100, window=entry2)

# duration
entry3 = tk.Entry(root)
canvas1.create_window(110, 150, window=entry3)

# priority
entry4 = tk.Entry(root)
canvas1.create_window(390, 150,window=entry4)

# student class
entry5 = tk.Entry(root)
canvas1.create_window(110, 200, window=entry5)

# location
entry6 = tk.Entry(root)
canvas1.create_window(390, 200, window=entry6)

# date & time
entry7 = tk.Entry(root)
canvas1.create_window(110, 250, window=entry7)

def get_exam_data():
    """
    appends exam data inputted by user to a master exam list
    """
    global scheduleMatrix
    global exams
    global courseCode
    exam = exam_scheduler.Exam()
    
    exam.course_code = entry1.get()
    courseCode = exam.course_code
    
    exam.instructor = entry2.get()
    
    exam.duration = entry3.get()
   
    exam.priority = entry4.get()
    
    exam.student_class = entry5.get()
    
    exam.location = entry6.get()
    
    exam.date_time = entry7.get()
    
    exams.append(exam)
    print("num exams ", len(exams))
    conflict = exam_scheduler.schedule_exam(exam, scheduleMatrix, availability, day_times)
    print("EXAM location ", exam.location)
    overload = exam_scheduler.overload(scheduleMatrix, exams)
    
    if len(overload) >= 3:
        print('overload found')
        prioritylabel = tk.Label(root, text="Overload for class of '"+exam.student_class)
        prioritylabel.config(font=('helvetica',12))
        canvas1.create_window(270, 375, window=prioritylabel)
    else:
        print('no overload')
        prioritylabel = tk.Label(root, text='No Overload                ')
        prioritylabel.config(font=('helvetica',12))
        canvas1.create_window(270, 375, window=prioritylabel)
        
    if conflict:
        print('conflict found')
        prioritylabel = tk.Label(root, text='Conflict found!')
        prioritylabel.config(font=('helvetica',12))
        canvas1.create_window(250, 350, window=prioritylabel)
    else:
    
        prioritylabel = tk.Label(root, text='No conflicts')
        prioritylabel.config(font=('helvetica',12))
        canvas1.create_window(250, 350, window=prioritylabel)
    
    label6 = tk.Label(root, text= '                                                                                                                   ',font=('helvetica', 12))
    canvas1.create_window(250, 300, window=label6)

    
    label6 = tk.Label(root, text= 'Exam for ' + exam.course_code + ' is: '\
    + exam.date_time+' at: '+exam.location,font=('helvetica', 12))
    canvas1.create_window(250, 300, window=label6)
    
    with open("schedule_file.txt", 'a') as schedule_file:
        
        schedule_file.write("\n")
        schedule_file.write(exam.course_code+"\t")
        schedule_file.write(exam.date_time+"     ")
        schedule_file.write(exam.location+"     ")
        schedule_file.write(exam.instructor+"            ")
        schedule_file.write(exam.priority+"             ")
        schedule_file.write(exam.duration+"\t")
        schedule_file.write(exam.student_class)
        
    return exams
    
    
def delete_exam():
    """
    deletes the exam specified by user input (course code)
    """
    global exams
    global courseCode
    courseCode = entry1.get()
    
    i = -1
    for e in exams:
        i += 1
        if e.course_code == courseCode:
            break
            
    print("DELETING ", i)
    if i != -1:
        del exams[i]
        deletelabel = tk.Label(root, text='Deleted '+courseCode)
        deletelabel.config(font=('helvetica',12))
        canvas1.create_window(250, 400, window=deletelabel)
    
      

# BUTTON THAT RUNS get_exam_data() TO COLLECT USER INPUT
button1 = tk.Button(text='Schedule Exam', command=get_exam_data)
canvas1.create_window(250, 450, window=button1)

course_code = entry1.get()

# BUTTON THAT RUNS delete_exam() TO DELETE EXAM SPECIFIED BY USER
button2 = tk.Button(text='Delete Exam', command=delete_exam)
canvas1.create_window(100, 450, window=button2)



def main():

    global day_times
    global availability
    global scheduleMatrix
    
    # load availabilities
    (availability, day_times) = exam_scheduler.load_availability('availabilities.csv')
    # create schedule matrix
    scheduleMatrix = exam_scheduler.create_schedule_matrix(availability,day_times)    
    
    root.mainloop()
    
    
if __name__ == "__main__":
    main()