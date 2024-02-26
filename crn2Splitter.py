import pandas as pd

class crn2Splitter:
    @staticmethod
    def crn2Splitter(path_to_schedule, output_file_path):
        start_time = pd.Timestamp.now()
        df_combined_crn2 = pd.read_excel(path_to_schedule)

        split_rows = []


        for _, row in df_combined_crn2.iterrows():
            # Split the CRN2 column into individual CRNs
            crns = row['CRN2'].split('-')
            
            # For each CRN, create a new row with the same data as the original row but with the CRN changed
            for crn in crns:
                new_row = row.copy()
                new_row['CRN'] = crn  
                split_rows.append(new_row)

        df_split = pd.DataFrame(split_rows)

        df_split.to_excel(output_file_path, index=False)

        end_time = pd.Timestamp.now()
        print(f"Execution time to split CRN2's: {(end_time - start_time).total_seconds()} seconds")

        return df_split
    

