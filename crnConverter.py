import pandas as pd
import time

class crnConverter:
    
    def crnConverter(path_to_f23_students, save_path):
        start_time = time.time()
        
        
        df_students = pd.read_excel(path_to_f23_students)
        
        
        df_students_filtered = df_students[(df_students['CREDIT'] != 0)]
       
        # Group by instructor and title, and combine CRNs
        combined_crn = df_students_filtered.groupby(['INSTRUCTOR', 'TITLE'])['CRN'].apply(
            lambda x: '-'.join(sorted(set(x.astype(str))))
        ).reset_index()

        
        combined_crn.rename(columns={'CRN': 'CRN2'}, inplace=True)

        # Merge the CRN2 data with the original DataFrame
        
        merged_df = pd.merge(df_students, combined_crn, on=['INSTRUCTOR', 'TITLE'], how='left')

       
        merged_df.to_excel(save_path, index=False)

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time to convert CRNs to CRN2s: {execution_time} seconds") 

        return merged_df.head()
