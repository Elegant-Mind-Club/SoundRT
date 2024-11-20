import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Scatter plot of means with SEM error bars and y=x reference line.')
    parser.add_argument('file_lists', nargs='+', type=str, help='Pairs of CSV files and an ID number separated by commas, e.g., "visual1.csv,auditory1.csv,1 visual2.csv,auditory2.csv,2"')
    args = parser.parse_args()

    for list in args.file_lists:
        try:
            output, survey, participant_number = list.split(',')
        except ValueError:
            print(f"Error: File pair '{list}' is not in the correct format. Ensure it is in 'file1,file2,#' format.")
            continue
        try:
            number = int(float(participant_number))
        except (ValueError, TypeError):
            return None
        output = output.strip()
        survey = survey.strip()
        output1 = pd.read_csv(output)
        survey1 = pd.read_csv(survey)
        maxrows = len(survey1)
        for rows in range(0, maxrows):
            if survey1.iloc[rows, 1] == number:
                participant_row = rows
                break
        survey_row = survey1.iloc[participant_row]
        survey_data_points = survey_row.tolist()
        output1['Gender'] = survey_data_points[2]
        output1['VideoGames'] = survey_data_points[3]
        output1['Music'] = survey_data_points[4]
        output1['Exercise'] = survey_data_points[5]
        output1['ToneDeafness'] = survey_data_points[6]

    output1.to_csv(output, index=False)

if __name__ == "__main__":
    main()

