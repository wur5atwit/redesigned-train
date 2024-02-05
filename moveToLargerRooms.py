import pandas as pd
import time

class moveToLargerRooms:
    def optimize_room_assignments(possible_schedule_path, room_capacities_path, output_file_path):
        start_time = time.time()
        exam_schedule = pd.read_excel(possible_schedule_path)
        room_capacities = pd.read_excel(room_capacities_path)

        room_capacities.rename(columns={'ROOM NAME': 'Room', 'CAPACITY': 'Capacity'}, inplace=True)
        
        # Ensure ANXC106 is excluded from the general list of available rooms
        room_capacities = room_capacities[room_capacities['Room'] != 'ANXCN106']

        updated_exams = []

        for _, exam in exam_schedule.iterrows():
            original_room = exam['Final Exam Room']
            if original_room == 'ANXCN106':
                # If the original room is ANXC106, keep it as is
                exam['New Assigned Room'] = 'ANXCN106'
            else:
                # Attempt to assign a new room
                suitable_rooms = room_capacities[room_capacities['Capacity'] >= exam['Count']].copy()
                if not suitable_rooms.empty:
                    # Assign the first suitable room based on capacity
                    exam['New Assigned Room'] = suitable_rooms.iloc[0]['Room']
                    # Remove the assigned room from future consideration
                    room_capacities = room_capacities[room_capacities['Room'] != suitable_rooms.iloc[0]['Room']]
                else:
                    # If no suitable room found, keep the original room
                    exam['New Assigned Room'] = original_room

            updated_exams.append(exam)

        updated_exam_schedule = pd.DataFrame(updated_exams)
        
        final_sorted_schedule = updated_exam_schedule.sort_values(by=['Count'], ascending=[False])

        final_sorted_schedule.to_excel(output_file_path, index=False)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time to optimize room assignments: {execution_time} seconds")

        return final_sorted_schedule

