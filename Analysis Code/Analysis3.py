import pandas as pd
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def gaussian(x, amp, mu, sigma):
    return amp * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

def process_data(df, df_name, coloration, coloration2, coloration3):
    
    df.columns = df.columns.str.strip()
    df['TimeDifference'] = df['ReactionTime'] - df['ObjShowTime']
    mean_value = df['TimeDifference'].mean()
    std_deviation = df['TimeDifference'].std()

    hist, bin_edges = np.histogram(df['TimeDifference'], bins=range(int(df['TimeDifference'].min()), 
                  int(df['TimeDifference'].max()) + 25, 25), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    popt, pcov = curve_fit(gaussian, bin_centers, hist, p0=[1, mean_value, std_deviation])

    fitted_amp, fitted_mean, fitted_std = popt
   
    sns.histplot(df['TimeDifference'], bins=bin_edges, kde=False, color=coloration, stat='density')
    plt.axvline(mean_value, color=coloration2, linestyle='solid', linewidth=1, label=f'{df_name} Stimulus - Mean: {mean_value:.2f} ms')
    plt.axvline(mean_value + std_deviation, color=coloration3, linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation:.2f} ms')
    plt.axvline(mean_value - std_deviation, color=coloration3, linestyle='dashed', linewidth=1)

    # Plot Gaussian fit
    x_fit = np.linspace(mean_value - 4*std_deviation, mean_value + 4*std_deviation, 1000)
    y_fit = gaussian(x_fit, *popt)
    plt.plot(x_fit, y_fit, color=coloration3, linewidth=2, label=f'Gaussian Fit {df_name}: μ = {fitted_mean:.2f} ms, σ = {fitted_std:.2f} ms')



file_path = r'/Users/taneeshkondapally/Documents/GitHub/SoundRT/Sound Files/Data/Auditory-3RCEG/AAppend-Auditory3RCEG-N=4.csv' # INSERT FILE NAMES TO ANALYZE HERE
file_path2 = r'/Users/taneeshkondapally/Documents/GitHub/SoundRT/Vision Files/VData/rgb/RTProcessing/AAppendrgb-N=4.csv'
data = pd.read_csv(file_path, delimiter=',')
data2 = pd.read_csv(file_path2, delimiter=',')
data_name = "Auditory"
data2_name = "Visual"
OneGColor = '#FF8080'
OneSColor = '#800000'
OneFColor = '#FF0000'
TwoGColor = '#80FF80'
TwoSColor = '#008000'
TwoFColor = '#00FF00'
'/Users/taneeshkondapally/Documents/GitHub/SoundRT/Sound Files/Data/Auditory-SRC/AAppend-AuditorySRC-N=4.csv'
plt.figure(figsize=(10, 6))
process_data(data, data_name, OneGColor, OneSColor, OneFColor)
process_data(data2, data2_name, TwoGColor, TwoSColor, TwoFColor)

plt.title('Histogram for Auditory vs. Visual Stimuli - 3 Stimuli, N=4')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 700)
plt.tight_layout()
plt.show()