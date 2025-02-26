import argparse
import pandas as pd
import numpy as np

# FOR EASE: JUST PASS THROUGH COMMAND LINE 'python3 {code file path} {source file path} {destination file path}
# SECOND THING: WHENEVER RUNNING THIS PROGRAM, RENAME THE DESTINATION FILE AFTER THE PATH --> ADD 1 TO THE LAST NUMBER IN THE FILE (GIVING US OUR N NUMBER)

def read_means_sem_from_csv(file_path):
    df = pd.read_csv(file_path)
    df['TimeDifference'] = df['ReactionTime'] - df['ObjShowTime']
    listLength = df['TimeDifference'].shape[0]
    means = [df['TimeDifference'].mean().tolist()]
    sems = [(df['TimeDifference'].std() / np.sqrt(listLength)).tolist()]
    return means, sems

def main():
    parser = argparse.ArgumentParser(description='Scatter plot of means with SEM error bars and y=x reference line.')
    parser.add_argument('file_pairs', nargs='+', type=str, help='Pairs of CSV files separated by a comma, e.g., "visual1.csv,auditory1.csv visual2.csv,auditory2.csv"')
    args = parser.parse_args()

    data_set = []
    out_file = '/Users/taneeshkondapally/Documents/GitHub/SoundRT/MeanAppendTouchVisionSR.csv' # CHANGE THIS LINE IF YOU'RE RUNNING IT AWAY FROM MY LAPTOP
    for pair in args.file_pairs:
        try:
            file_visual, file_auditory = pair.split(',')
        except ValueError:
            print(f"Error: File pair '{pair}' is not in the correct format. Ensure it is in 'file1,file2' format.")
            continue
        
        file_visual = file_visual.strip()
        file_auditory = file_auditory.strip()
        
        try:
            means_visual, sems_visual = read_means_sem_from_csv(file_visual)
            means_auditory, sems_auditory = read_means_sem_from_csv(file_auditory)
        except Exception as e:
            print(f"Error reading data from files '{file_visual}' and '{file_auditory}': {e}")
            continue
        
        data_set.append((means_visual, sems_visual, means_auditory, sems_auditory))
    data = pd.DataFrame(data_set, columns=["Visual Mean", "Visual SEM", "Auditory Mean", "Auditory SEM"])
    data.to_csv(out_file, index=False)

if __name__ == "__main__":
    main()