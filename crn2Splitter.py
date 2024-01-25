import pandas as pd
import time

class crn2Splitter:
    @staticmethod
    def crn2Splitter(path_to_combined_crn2, output_file_path):
        start_time = time.time()
        df_combined_crn2 = pd.read_excel(path_to_combined_crn2)

        # Preparing a list to hold new rows
        split_rows = []

        for index, row in df_combined_crn2.iterrows():
            # Splitting CRN2 into original CRNs
            crns = row['CRN2'].split('-')

            for crn in crns:
                # Creating a new row for each CRN
                new_row = row.copy()
                new_row['CRN'] = crn  
                split_rows.append(new_row)

        # Creating a new DataFrame from the list of new rows
        df_split = pd.DataFrame(split_rows)
        
        df_split = df_split[['CRN', 'INSTRUCTOR', 'SUBJECT']]

        df_split.to_excel(output_file_path, index=False)


        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time to split crn2's: {execution_time} seconds") 

        return df_split
