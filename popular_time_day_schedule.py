import pandas as pd
def swap_courses_within_same_day(schedule_df, day, most_popular_time_slot):
    outcome = {
        'day': day,
        'swap_made': False,
        'message': "",
        'details': {
            'max_students_crn': None,
            'target_crn': None,
            'original_time': None,
            'new_time': None
        }
    }

    classes_on_day = schedule_df[schedule_df['EXAM DAY'] == day]
    if classes_on_day.empty:
        outcome['message'] = f"No classes found for Day {day}."
        return outcome

    class_at_popular_time = classes_on_day[classes_on_day['EXAM TIME'] == most_popular_time_slot]
    max_students_class = classes_on_day.sort_values('Count', ascending=False).head(1)

    if max_students_class.empty:
        outcome['message'] = f"No classes on Day {day} to consider for swapping."
        return outcome

    max_students_class_idx = max_students_class.index[0]
    max_students_crn = schedule_df.loc[max_students_class_idx, 'CRN2']

    if class_at_popular_time.empty or max_students_class_idx in class_at_popular_time.index:
        outcome['message'] = f"Day {day}: No swap needed or possible for '{max_students_crn}'."
    else:
        class_at_popular_time_idx = class_at_popular_time.index[0]
        target_crn = schedule_df.loc[class_at_popular_time_idx, 'CRN2']

        # Recording original and new times for the swap
        original_time = schedule_df.loc[max_students_class_idx, 'EXAM TIME']
        schedule_df.loc[max_students_class_idx, 'EXAM TIME'] = most_popular_time_slot
        schedule_df.loc[class_at_popular_time_idx, 'EXAM TIME'] = original_time

        outcome['swap_made'] = True
        outcome['message'] = f"Day {day}: Swapped '{max_students_crn}' with '{target_crn}' to move to time slot {most_popular_time_slot}."
        outcome['details'] = {
            'max_students_crn': max_students_crn,
            'target_crn': target_crn,
            'original_time': original_time,
            'new_time': most_popular_time_slot
        }

    return outcome



def popular_time_day_schedule(possible_schedule_df, popular_day_number, least_popular_day_number, most_popular_time_slot):
    newtime_mapping = {
        (1, 1): 0, (2, 1): 1, (2, 2): 2, (3, 1): 3, (3, 2): 4, (1, 2): 5,
        (4, 1): 6, (4, 2): 7, (2, 3): 8, (4, 3): 9, (3, 3): 10, (1, 3): 11,
        (2, 4): 12, (1, 4): 13, (3, 4): 14, (4, 4): 15
    }
    possible_schedule_df['Day Letter'] = possible_schedule_df['EXAM DAY'].map(lambda x: {1: 'A', 2: 'B', 3: 'C', 4: 'D'}.get(x))
    students_per_lettered_day = possible_schedule_df.groupby('Day Letter')['Count'].sum()

    most_students_day_letter = students_per_lettered_day.idxmax()
    least_students_day_letter = students_per_lettered_day.idxmin()

    print(f"Day {most_students_day_letter} has the most students and is assigned to popular day {popular_day_number}.")
    print(f"Day {least_students_day_letter} has the least students and is assigned to least popular day {least_popular_day_number}.")

    possible_schedule_df.loc[possible_schedule_df['Day Letter'] == most_students_day_letter, 'EXAM DAY'] = popular_day_number
    possible_schedule_df.loc[possible_schedule_df['Day Letter'] == least_students_day_letter, 'EXAM DAY'] = least_popular_day_number

    swap_outcomes = []  # Collect outcomes of all swaps
    for day in possible_schedule_df['EXAM DAY'].unique():
        outcome = swap_courses_within_same_day(possible_schedule_df, day, most_popular_time_slot)
        swap_outcomes.append(outcome)

    # Here you could log, print, or further process swap_outcomes as needed
    for outcome in swap_outcomes:
        print(outcome['message'])  # Example of utilizing the swap outcome messages

    possible_schedule_df['NewTime'] = possible_schedule_df.apply(lambda row: newtime_mapping.get((row['EXAM DAY'], row['EXAM TIME'])), axis=1)
    
    return possible_schedule_df


def check_room_conflicts(possible_schedule_df, room_capacities_df):
    
    merged_df = pd.merge(possible_schedule_df, room_capacities_df, left_on='Final Exam Room', right_on='ROOM NAME', how='left')

    # Identify conflicts
    conflict_df = merged_df[merged_df['Count'] > merged_df['CAPACITY']]
    if not conflict_df.empty:
        print("Room conflicts found where the count exceeds room capacity:")
        print(conflict_df[['Final Exam Room', 'Count', 'CAPACITY']])
    else:
        print("No room conflicts found.")
    return conflict_df

possible_schedule_path = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx" 
room_capacities_path = r"C:\Users\richa\Downloads\COOP\RoomCapacities.xlsx"
possible_schedule_df = pd.read_excel(possible_schedule_path)
room_capacities_df = pd.read_excel(room_capacities_path)

optimized_schedule_df = popular_time_day_schedule(possible_schedule_df, 2, 4, 2)

# After optimizing the schedule, check for room conflicts
conflict_df = check_room_conflicts(optimized_schedule_df, room_capacities_df)

optimized_output_path = "popular_time_day_schedule.xlsx"
optimized_schedule_df.to_excel(optimized_output_path, index=False)
print(f"Optimized schedule saved to {optimized_output_path}")

if not conflict_df.empty:
    conflict_output_path = "room_conflicts.xlsx"
    conflict_df.to_excel(conflict_output_path, index=False)
    print(f"Room conflicts saved to {conflict_output_path}")
