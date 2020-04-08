"""
Created on Tue Mar 31 13:43:11 2020

EXAM SCHEDULER PROJECT
RIDAM LOOMBA

exam_scheduler.py
"""

import csv

MAX_COURSE_LENGTH = 6
MAX_LOC_LENGTH = 6
MAX_DAY_LENGTH = 9
NUM_DAYS = 15
MAX_NAME = 256
NUM_LOCATIONS = 40
NUM_EXAM_PERIODS = 3



class Location:
    """
    definine the properties of a locaion
    """
    name = ""
    daytimes = []
    
    def __init__(self,name, daytimes):
        self.name = name
        self.daytimes = daytimes

class Exam:
    """
    definine the properties of an exam
    """
    course_code = ""
    location = ""
    instructor = ""
    start_time = ""
    duration = ""
    priority = ""
    student_class = ""   
    date_time = ""   


def load_availability(csv_file):
    """
    loads data from an availability text file and returns two lists that hold
    the availability data of each location and each date&time
    """
    availability = []
    day_times = []

    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                day_times = row[1:]
                line_count += 1
            else:
                availability.append(Location(row[0],row[1:]))
                line_count += 1
    
    return (availability, day_times)
    

def load_exams(csv_file):
    """
    loads a file with details about each course's exam. 
    returns a list of all courses with exams to be scheduled
    """
    exams = []

    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                exam = Exam()
                
                exam.course_code = row[0]
                exam.instructor= row[2]
                exam.location = row[3]
                exam.duration = row[4]
                exam.priority = row[5]
                exam.student_class = row[6] 
                exams.append(exam)
                
                line_count += 1
    return exams
 
def deleteExam(course_code, exams):
    """
    takes a course code and the list of all exams as an input and deletes the
    exam associate with the inputted course code.
    """
    i = -1
    for e in exams:
        i += 1
        if e.course_code == course_code:
            break

    if i != -1:
        del exams[i]
        

def printExamSchedule(studentClass, exams):
    """
    prints the exam schedule for a specific student class
    """
    print("Exam Schedule")
    print("-----------------------------------------------------------------------------------------------------------------")
    print("Course Code".ljust(15)[:15]+"Date/Time".ljust(17)[:17]+"Location".ljust(21)[:21]+"Instructor".ljust(17)[:17]+"Duration".ljust(15)[:15]+"Priority".ljust(15)[:15]+"Student Class")
    print()
    for exam in exams:
        if exam.student_class == studentClass:
            print(exam.course_code.ljust(15)[:15] + exam.date_time.ljust(17)[:17]+exam.location.ljust(21)[:21]+exam.instructor.ljust(17)[:17]+exam.duration.ljust(15)[:15]+exam.priority.ljust(15)[:15]+exam.student_class)
            
            
def printEntireExamSchedule(exams):
    """
    prints the entire exam schedule given the list of exams
    """
    print("Exam Schedule")
    print("-----------------------------------------------------------------------------------------------------------------")
    print("Course Code".ljust(15)[:15]+"Date/Time".ljust(17)[:17]+"Location".ljust(21)[:21]+"Instructor".ljust(17)[:17]+"Duration".ljust(15)[:15]+"Priority".ljust(15)[:15]+"Student Class")
    print()
    for exam in exams:
        print(exam.course_code.ljust(15)[:15] + exam.date_time.ljust(17)[:17]+exam.location.ljust(21)[:21]+exam.instructor.ljust(17)[:17]+exam.duration.ljust(15)[:15]+exam.priority.ljust(15)[:15]+exam.student_class)
            
    
    
    
def sort_by_priority(exams):
    """
    sorts the list of inputted exams by priority
    """
    
    # SELECTION SORT
    for i in range(len(exams)): 

        min_idx = i 
        for j in range(i+1, len(exams)): 
            if exams[min_idx].priority > exams[j].priority: 
                min_idx = j 
                
        exams[i], exams[min_idx] = exams[min_idx], exams[i] 
                

def load_scheduling_matrix(exams, scheduleMatrix, availability, day_times):
        """
        populates the scheduling matrix with exam data
        """
        
        m = 0
            
        # i = date time
        # j = location
        for i in range(len(scheduleMatrix)):
            for j in range(len(scheduleMatrix[i])):
                if m < len(exams):
                    if availability[j].daytimes[i] == '1': 
                        found_student = False
                        for z in range(j):
                            if exams[m].student_class == scheduleMatrix[i][z].student_class:
                                found_student = True
                                break
                        if found_student:
                            break
                        exams[m].location =  availability[j].name
                        exams[m].date_time = day_times[i]
                        scheduleMatrix[i][j] = exams[m]
    
                        m += 1
                
        
def schedule_exam(exam, scheduleMatrix, availability, day_times):
        """
        schedules exams and searches for coflicts. 
        returns a conflict boolean: True if conflict is found, 
        False if no conflict is found.
        """
        
        conflict = False
            
        use_this_location = ""
        use_this_date_time = ""
        # i = date time
        # j = location
        if exam.location != "":
            # if given a location from user
            use_this_location = exam.location
            
        if exam.date_time != "":
            # if given a date/time from user
            use_this_date_time = exam.date_time
            
        # SCHEDULING
        for i in range(len(scheduleMatrix)):
            for j in range(len(scheduleMatrix[i])):
                if availability[j].daytimes[i] == '1': 
                    if exam.location != "" and exam.date_time != "" and exam.location == \
                    scheduleMatrix[i][j].location and exam.date_time == scheduleMatrix[i][j].date_time:
                        # FOUND CONFLICT
                        conflict = True
                    else:
                        found_student = False
                        for z in range(j):
                            if exam.student_class == scheduleMatrix[i][z].student_class:
                                found_student = True
                                break
                        if found_student:
                            break
                        if scheduleMatrix[i][j].location == "":
                            # location and time are not specified by yser
                            if use_this_location != "" and use_this_date_time == "":
                                if availability[j].name == use_this_location:
                                    exam.date_time = day_times[i]
                                    scheduleMatrix[i][j] = exam
                                    return False
                            elif use_this_location != "" and use_this_date_time != "":
                                if availability[j].name == use_this_location and day_times[i] == use_this_date_time:
                                    scheduleMatrix[i][j] = exam
                                    return False
                            elif use_this_location == "" and use_this_date_time != "":
                                if day_times[i] == use_this_date_time:
                                    exam.location = availability[j].name
                                    scheduleMatrix[i][j] = exam
                                    return False
                            elif use_this_location == "" and use_this_date_time == "":
                                exam.location = availability[j].name
                                exam.date_time = day_times[i]
                                scheduleMatrix[i][j] = exam
                                return False
    
        return conflict


def create_schedule_matrix(availability, day_times):
    """
    creates a blank schedule matrix based on location/time&date availabilities
    """
    num_locations = len(availability)
    num_timeslots = len(day_times)
    scheduleMatrix = [[Exam() for j in range(num_locations)] for i in range(num_timeslots)]   
    return scheduleMatrix
    
def overload(scheduleMatrix, exams):
    """
    searches for an overloaded schedule for any class
    """
    exam_overload = []
    found = False
    counter = 0
    
    for exam in exams:
        counter = 0
        for i in range(len(scheduleMatrix)):
            found = False
            for j in range(len(scheduleMatrix[i])):
                      
                if exam.student_class == scheduleMatrix[i][j].student_class:
                    found = True
                    counter += 1
            if found == True:
                if counter >= 3:
                    # OVERLOAD
                    exam_overload.append(exam)
            else:
                counter = 0
                      
    return exam_overload

    

schedule = True
exams = [] #sort by priority
edit = ""

if __name__ == "__main__":
    """
    FOR TESTING PURPOSES ONLY
    """
    eng_exams = load_exams('eng_exam.csv')
    (availability, day_times) = load_availability('availabilities.csv')
    schedule = create_schedule_matrix(availability, day_times)
    
    #for h in range(len(day_times)):
    #    print("h: ", h, day_times[h])
    #for dt in day_times:
    #    print(dt)
    """
    for a in availability:
        print(a.name)
        for d in a.daytimes:
            print(d)
    """
    sort_by_priority(eng_exams)
    
    #for exam in eng_exams:
    #    print(exam.course_code, exam.location, exam.priority)
    
    #deleteExam("CHE260H1", eng_exams)
    
    #"AFTER DELETEING"
    #for exam in eng_exams:
    #    print('d', exam.course_code, exam.location, exam.priority)
    
    #print(eng_exams)
    load_scheduling_matrix(eng_exams, schedule, availability, day_times)
    
    studentClass = "21"
    
   # printEntireExamSchedule(eng_exams)
    
    # PRINT STUDENT
    printExamSchedule(studentClass, eng_exams)
    
