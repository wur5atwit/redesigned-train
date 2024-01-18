Function1 designed to process and combine data from two Excel spreadsheets: 'Students Excel File'. Student file needs "title", "course_instructor", "CRN" in the columns. 
Grouping and Combining: It groups the data by 'course_instructor' and 'title', and combines CRNs for each group into a single string (CRN2), ensuring no duplicate CRNs within each group.


Count Faculty Conflict Function needs 'Exam Schedule'. File needs "EXAM DAY", "NewTime", "INSTRUCTOR" in the columns for inputs.
Designed to identify and count scheduling conflicts for faculty members based on exam schedules.


Count Student Conflict Function needs 'Student Schedule' and 'Exam Schedule'. Student file needs "CRN", "STUDENT NAME" as inputs. 'Exam Schedule' needs "CRN2", "EXAM DAY", "NewTime" as inputs.
Designed to calculate and identify conflicts in student exam schedules. It checks for instances where a student is scheduled to take multiple exams at the same time.


Count Room Conflict Function needs 'Room Capacities' and 'Exam Schedule'. Room file needs "ROOM NAME", "CAPACITY" as inputs. Exam Schedule needs "Count", "Final Exam Room" as inputs.
Designed to identify and quantify instances where the number of students scheduled for an exam exceeds the capacity of the assigned room. This function helps to ensure that exam room allocations are adequate for the number of students taking the exam.


Count 3 in 1 Function needs 'Student Schedule' and 'Exam Schedule'. Student file needs "CRN", "STUDENT NAME" as inputs. Exam Schedule needs "CRN2", "EXAM DAY" as inputs.
Designed to identify and count the number of students who have more than three exams scheduled on a single day. 


Count Double Booked Room Function needs 'Exam Schedule'. File needs "Final Exam Room", "EXAM DAY", "NewTime" as inputs.
Method is designed to detect and count instances of double booking in exam rooms. This occurs when an exam room is scheduled to be used by more than one exam at the same time on the same day.

**HOW TO RUN**
## Installation

To install the required Python packages, run the following command in the console:
pip install -r requirements.txt

Run the main.py file and input the files that are asked.
