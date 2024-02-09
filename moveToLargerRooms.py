import pandas as pd
import time

class moveToLargerRooms:
    def optimize_room_assignments(possible_schedule_path, room_capacities_path, output_file_path):
        start_time = time.time()
        exam_schedule = pd.read_excel(possible_schedule_path)
        room_capacities = pd.read_excel(room_capacities_path)

        # Prepare room capacities, excluding 'ANXCN106', and sort by capacity in descending order
        room_capacities.rename(columns={'ROOM NAME': 'Room', 'CAPACITY': 'Capacity'}, inplace=True)
        large_rooms = room_capacities[room_capacities['Room'] != 'ANXCN106'].sort_values(by='Capacity', ascending=False)

        # Initialize a dictionary to keep track of room assignments for each NewTime
        assigned_rooms_per_newtime = {}

        for newtime in sorted(exam_schedule['NewTime'].unique()):
            assigned_rooms_per_newtime[newtime] = set()
            exams_at_newtime = exam_schedule[exam_schedule['NewTime'] == newtime]

            for index, exam in exams_at_newtime.iterrows():
                if exam['Final Exam Room'] == 'ANXCN106':
                    # Keep 'ANXCN106' assignments unchanged
                    exam_schedule.at[index, 'New Assigned Room'] = 'ANXCN106'
                else:
                    # Assign the next largest available room not yet used for this NewTime
                    for _, room in large_rooms.iterrows():
                        if room['Room'] not in assigned_rooms_per_newtime[newtime]:
                            exam_schedule.at[index, 'New Assigned Room'] = room['Room']
                            assigned_rooms_per_newtime[newtime].add(room['Room'])
                            break

        
        final_sorted_schedule = exam_schedule.sort_values(by=['NewTime', 'Count'], ascending=[True, False])

        
        final_sorted_schedule.to_excel(output_file_path, index=False)

        end_time = time.time()
        print(f"Execution time to optimize room assignments: {end_time - start_time} seconds")

        return final_sorted_schedule

