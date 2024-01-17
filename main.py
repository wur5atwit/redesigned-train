import pandas as pd
from function1 import function1
from function2 import function2
from function3 import function3
class Schedule:
    
    # Combine CRN2
    callFunction1 = function1.crn2Sorter()

    #Find Faculty conflicts
    faculty_conflicts = function2.count_faculty_conflicts()
    print(f"Faculty Conflicts: {faculty_conflicts}")

    #Find student conflicts
    student_conflicts, students_with_conflicts = function2.count_student_conflicts()
    print(f"Number of student conflicts: {student_conflicts}")
    if student_conflicts > 0:
        print("Students with conflicts:", students_with_conflicts)

    #Find room too small conflicts
    room_conflicts, conflict_details = function2.count_room_conflicts()
    print(f"Number of room too small conflicts: {room_conflicts}")
    if room_conflicts > 0:
        print("Details of room conflicts:\n", conflict_details)
    
    #Find 3 in 1 conflicts
    students_with_multiple_exams, multiple_exams_details = function2.count_students_with_multiple_exams()
    print(f"Number of students with more than three exams in a single day: {room_conflicts}")
    if room_conflicts > 0:
        print("Details of students with multiple exams:\n", conflict_details)

    #Find double booked conflicts
    double_booked_rooms, double_booking_details = function2.count_double_booked_rooms()
    print(f"Number of double booked rooms: {double_booked_rooms}")
    if double_booked_rooms > 0:
        print("Details of room conflicts:\n", double_booking_details)


    optimized_schedule = function3.optimize_room_assignments()
    
    

# #To call the function and see the output
# output = Schedule.function1()

# #count faculty
# num_conflicts = Schedule.count_faculty_conflicts()

# print(f"Number of faculty conflicts: {num_conflicts}")

# # To call the function and get the number of student conflicts and the list of students with conflicts
# num_conflicts, students_with_conflicts = Schedule.count_student_conflicts()
# 


# num_students, students_with_multiple_exams = Schedule.count_students_with_multiple_exams()




# # To call the function and get the number of room conflicts and the details of conflicts
# num_conflicts, conflict_details = Schedule.count_room_conflicts()





# Usage
# optimizer = ScheduleOptimizer(r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx", r"C:\Users\richa\Downloads\COOP\RoomCapacities.xlsx")
# optimized_schedule = optimizer.optimize_room_assignments()



    

