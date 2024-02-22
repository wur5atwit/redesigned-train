import pandas as pd

def moveCrnTime(crn2_str, exam_schedule_path, output_path):
    
    newtime_mapping = {
        0: (1, 1), 1: (2, 1), 2: (2, 2), 3: (3, 1), 4: (3, 2), 5: (1, 2),
        6: (4, 1), 7: (4, 2), 8: (2, 3), 9: (4, 3), 10: (3, 3), 11: (1, 3),
        12: (2, 4), 13: (1, 4), 14: (3, 4), 15: (4, 4)
    }

    
    exam_schedule = pd.read_excel(exam_schedule_path)

    # Split the input CRN2 string into individual CRN2 values
    crn2_list = crn2_str.split('-')

    # Find rows where any part of the CRN2 string matches
    crn2_exists = exam_schedule['CRN2'].apply(lambda x: any(crn2_part in str(x).split('-') for crn2_part in crn2_list))

    if not crn2_exists.any():
        print(f"CRN2 {crn2_str} not found in the schedule.")
        return

    
    newtime = int(input("Enter the new time (0-15): "))
    if newtime not in newtime_mapping:
        print("Invalid newtime. Please enter a value between 0 and 15.")
        return

    
    new_day, new_time = newtime_mapping[newtime]

    # Update the schedule for rows matching the specified CRN2(s)
    exam_schedule.loc[crn2_exists, 'EXAM DAY'] = new_day
    exam_schedule.loc[crn2_exists, 'EXAM TIME'] = new_time
    
    exam_schedule.loc[crn2_exists, 'NewTime'] = newtime

    
    exam_schedule.to_excel(output_path, index=False)
    print(f"Updated schedule saved to {output_path}")


exampath = "C:/Users/richa/Downloads/COOP/Possible_Schedule.xlsx"
outputpath = "C:/Users/richa/Downloads/COOP/output_updated.xlsx"


run = moveCrnTime("12264-12265-12266-12267-12778", exampath, outputpath)
