import pandas as pd

class function4:
    @staticmethod
    def crn2Splitter(path_to_combined_crn2):
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

        df_split.to_excel("Seperated_Crns.xlsx", index=False)

        return df_split
