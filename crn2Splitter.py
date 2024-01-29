import pandas as pd
import time

class crn2Splitter:
    @staticmethod
    def crn2Splitter(path_to_combined_crn2, output_file_path):
        start_time = time.time()
        df_combined_crn2 = pd.read_excel(path_to_combined_crn2)

       
        split_rows = []

        for _, row in df_combined_crn2.iterrows():
            
            crns = row['CRN2'].split('-')
            
            for crn in crns:
                # Creating a new row for each CRN
                new_row = row.copy()
                new_row['CRN'] = crn  # Adding the split CRN
                split_rows.append(new_row)

    
        df_split = pd.DataFrame(split_rows)
        
        # Rearranging columns as needed
        column_order = ['CRN', 'CRN2', 'Count', 'SUBJECT', 'COURSE NUMBER', 'INSTRUCTOR', 'Name', 'NewTime', 'Final Exam Room', 'EXAM DAY', 'EXAM TIME']
        df_split = df_split[column_order]  

        
        df_split.to_excel(output_file_path, index=False)

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time to split CRN2's: {execution_time} seconds") 

        return df_split
