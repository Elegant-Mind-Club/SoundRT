import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np


# Function to calculate mean and SEM from a CSV file with raw data points
def read_means_sem_from_csv(file_path):
    df = pd.read_csv(file_path)
    df = df[df['Correct'] == 1]
    df['TimeDifference'] = df['ReactionTime'] - df['ObjShowTime']
    Q1 = df['TimeDifference'].quantile(0.25)
    Q3 = df['TimeDifference'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['TimeDifference'] >= lower_bound) & (df['TimeDifference'] <= upper_bound)]
    listLength = df['TimeDifference'].shape[0]
    means = [df['TimeDifference'].mean().tolist()]
    sems = [(df['TimeDifference'].std() / np.sqrt(listLength)).tolist()]
    return means, sems

# Argument parser setup
parser = argparse.ArgumentParser(description='Scatter plot of means with SEM error bars and y=x reference line.')
parser.add_argument('file_pairs', nargs='+', type=str, help='Pairs of CSV files separated by a comma, e.g., "visual1.csv,auditory1.csv visual2.csv,auditory2.csv"')
args = parser.parse_args()

# Read means and SEMs from each pair of files
paired_means = []
paired_sems = []
visual_means = []
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
    
    paired_means.append((means_visual, means_auditory))
    paired_sems.append((sems_visual, sems_auditory))
    visual_means.append(means_visual)

# Plotting the scatter plot
plt.figure(figsize=[10, 10])

# Scatter plot of the means
colors = plt.cm.rainbow(np.linspace(0, 1, len(paired_means)))
for i, ((means_visual, means_auditory), (sems_visual, sems_auditory)) in enumerate(zip(paired_means, paired_sems)):
    plt.scatter(means_visual, means_auditory, color=colors[i], label=f'Participant {i+1}')
    for mean_vis, sem_vis, mean_aud, sem_aud in zip(means_visual, sems_visual, means_auditory, sems_auditory):
        plt.errorbar(mean_vis, mean_aud, xerr=sem_vis, yerr=sem_aud, fmt='o', color=colors[i], ecolor='red', capsize=5)

# Adding y=x reference line
min_val = min(min(mean) for mean_pair in paired_means for mean in mean_pair)
max_val = max(max(mean) for mean_pair in paired_means for mean in mean_pair)
plt.plot([0, 500], [0, 500], linestyle='solid', color='green', label='y=x reference line')
plt.xlim(0, 500)
plt.ylim(0, 500)

# Adding labels and title
plt.title('2 Stimuli vs. 3 Stimuli - Auditory, N=10')
plt.xlabel('2 Stimuli (ms)')
plt.ylabel('3 Stimuli (ms)')
plt.legend()
plt.grid(False)
plt.tight_layout()
plt.show()