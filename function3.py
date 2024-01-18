import pandas as pd

class function3:
    @staticmethod
    def optimize_room_assignments(possible_schedule, room_capacities):
        possible_schedule = pd.read_excel(possible_schedule)
        room_capacities = pd.read_excel(room_capacities)

        # Add a column for original room assignments
        possible_schedule['Original Room'] = possible_schedule['Final Exam Room']

        # Initialize DataFrame to track room availability for each day
        available_rooms = room_capacities.copy()
        available_rooms['Available Days'] = available_rooms.apply(lambda x: list(range(1, 8)), axis=1)  # Assuming 7 days for exams

        # Iterate through each day and NewTime slot
        for day in possible_schedule['EXAM DAY'].unique():
            for new_time in possible_schedule['NewTime'].unique():
                exams_this_slot = possible_schedule[(possible_schedule['EXAM DAY'] == day) & (possible_schedule['NewTime'] == new_time)]
                exams_this_slot = exams_this_slot.sort_values(by='Count', ascending=False)
                
                for index, exam in exams_this_slot.iterrows():
                    current_room = exam['Final Exam Room']
                    current_capacity = available_rooms.loc[available_rooms['ROOM NAME'] == current_room, 'CAPACITY'].values[0]

                    # Filter for bigger available rooms
                    bigger_available_rooms = available_rooms[(available_rooms['CAPACITY'] > current_capacity) & 
                                                             (available_rooms['Available Days'].apply(lambda x: day in x))]
                    if not bigger_available_rooms.empty:
                        new_room = bigger_available_rooms.iloc[0]
                        possible_schedule.at[index, 'Final Exam Room'] = new_room['ROOM NAME']
                        # Update the available days for the new room
                        available_rooms.loc[available_rooms['ROOM NAME'] == new_room['ROOM NAME'], 'Available Days'] = available_rooms.loc[available_rooms['ROOM NAME'] == new_room['ROOM NAME'], 'Available Days'].apply(lambda x: [d for d in x if d != day])

                    # Update the available days for the current room
                    available_rooms.loc[available_rooms['ROOM NAME'] == current_room, 'Available Days'] = available_rooms.loc[available_rooms['ROOM NAME'] == current_room, 'Available Days'].apply(lambda x: [d for d in x if d != day])

        # Format unused rooms list
        unused_rooms_formatted = available_rooms.explode('Available Days')
        unused_rooms_formatted = unused_rooms_formatted.dropna(subset=['Available Days']).reset_index(drop=True)

        
        # Save the updated exam schedule and formatted unused rooms to Excel
        with pd.ExcelWriter("optimized_schedule.xlsx") as writer:
            possible_schedule.to_excel(writer, sheet_name='Optimized Schedule', index=False)
            unused_rooms_formatted.to_excel(writer, sheet_name='Formatted Unused Rooms', index=False)

        return possible_schedule
