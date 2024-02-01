
Student file needs these data: "STUDENT_NAME", "TITLE", "INSTRUCTOR", "CRN", "CREDIT"<br />
Exam Schedule needs these data: "CRN2", "INSTRUCTOR", "NEW_TIME", "EXAM_ROOM", EXAM_DAY<br />
Room capacities file needs these data: "ROOM_NAME", "CAPACITY"<br />

CRN Convert to CRN2 will take a file that contains CRN.<br />
It will turn CRN data into CRN2.<br />

Schedule Conflict checker will take in the Student file, Exam Schedule, and Room capacities file.<br />
Will check for conflicts with faculty, students, room size too small, and used rooms multiped times.<br /> 

Room optimizer will take in Exam Schedule and Room capacities file.<br />
Will give the biggest rooms to the biggest class sizes.<br />

CRN2 Separator will take in a file that contains CRN2.<br />
It will turn CRN2 data back into CRN.<br />

Merged student and exam schedule: "STUDENT_NAME", "CRN2", "CRN", "INSTRUCTOR", "CREDIT", "NEW_TIME", "EXAM_ROOM"<br />
--**HOW TO RUN**--
## Installation

To install the required Python packages, run the following command in the console:
pip install -r requirements.txt

Run the main.py file and input the files that are asked for.


