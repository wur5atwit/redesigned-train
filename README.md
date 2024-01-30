INPUTS NEEDED FOR:
Student File: "STUDENT_NAME", "TITLE", "INSTRUCTOR", "CRN", "CREDIT"<br />
Exam Schedule: "CRN2", "INSTRUCTOR", "NEW_TIME", "EXAM_ROOM"<br />
Room Capacities: "ROOM_NAME", "CAPACITY"<br />


**Function 1 needs Student file.**<br />
**Function 2 needs Student, Exam Schedule, and Room capacities file.**<br />
**Function 3 needs Exam Schedule, and Room capacities file.**<br />

Merged student and exam schedule: "STUDENT_NAME", "CRN2", "CRN", "INSTRUCTOR", "CREDIT", "NEW_TIME", "EXAM_ROOM"<br />
--**HOW TO RUN**--
## Installation

To install the required Python packages, run the following command in the console:
pip install -r requirements.txt

Run the main.py file and input the files that are asked.


## Infomation about functions
Function 1 combines CRN into CRN2.

Function 2:
Count Faculty Conflict Function Designed to identify and count scheduling conflicts for faculty members based on exam schedules.

Count Student Conflict Function Designed to calculate and identify conflicts in student exam schedules. It checks for instances where a student is scheduled to take multiple exams at the same time.

Count Room Conflict Function  Designed to identify and quantify instances where the number of students scheduled for an exam exceeds the capacity of the assigned room. This function helps to ensure that exam room allocations are adequate for the number of students taking the exam.

Count 3 in 1 Function  Designed to identify and count the number of students who have more than three exams scheduled on a single day. 

Count Double Booked Room Function Method is designed to detect and count instances of double booking in exam rooms. This occurs when an exam room is scheduled to be used by more than one exam at the same time on the same day.

Function 3:
Redos rooms for schedule giving the biggest room first to biggest class size.

