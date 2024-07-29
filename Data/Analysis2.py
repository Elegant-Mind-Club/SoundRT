import pandas as pd
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

file_path = r'/Users/taneeshkondapally/Downloads/Taneesh_SRrtData_2024-07-23.csv' # INSERT FILE NAMES TO ANALYZE HERE
file_path2 = r'/Users/taneeshkondapally/Downloads/Taneesh.2SrtData.2024-07-23.csv'
file_path3 = r'/Users/taneeshkondapally/Downloads/Taneesh.3SrtData.2024-07-23.csv'
data = pd.read_csv(file_path)
data2 = pd.read_csv(file_path2)
data3 = pd.read_csv(file_path3)

# Remove all trials with False in the 'Correct' column
filtered_data = data[data['Correct'] == True]

# Convert time columns to numeric
filtered_data['ObjShowTime'] = pd.to_numeric(filtered_data['ObjShowTime'])
filtered_data['ReactionTime'] = pd.to_numeric(filtered_data['ReactionTime'])

# Calculate ReactionTime - ObjShowTime
filtered_data['TimeDifference'] = filtered_data['ReactionTime'] - filtered_data['ObjShowTime']

# Remove 50 ms from all trials
filtered_data['TimeDifference'] = filtered_data['TimeDifference'] - 50

# Remove outliers beyond 1.5*IQR
Q1 = filtered_data['TimeDifference'].quantile(0.25)
Q3 = filtered_data['TimeDifference'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

filtered_data = filtered_data[(filtered_data['TimeDifference'] >= lower_bound) & (filtered_data['TimeDifference'] <= upper_bound)]

# Calculate mean and standard deviation
mean_value = filtered_data['TimeDifference'].mean()
std_deviation = filtered_data['TimeDifference'].std()

# Remove all trials with False in the 'Correct' column
filtered_data2 = data2[data2['Correct'] == True]

# Convert time columns to numeric
filtered_data2['ObjShowTime'] = pd.to_numeric(filtered_data2['ObjShowTime'])
filtered_data2['ReactionTime'] = pd.to_numeric(filtered_data2['ReactionTime'])

# Calculate ReactionTime - ObjShowTime
filtered_data2['TimeDifference'] = filtered_data2['ReactionTime'] - filtered_data2['ObjShowTime']

# Remove 50 ms from all trials
filtered_data2['TimeDifference'] = filtered_data2['TimeDifference'] - 50

# Remove outliers beyond 1.5*IQR
Q1 = filtered_data2['TimeDifference'].quantile(0.25)
Q3 = filtered_data2['TimeDifference'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

filtered_data2 = filtered_data2[(filtered_data2['TimeDifference'] >= lower_bound) & (filtered_data2['TimeDifference'] <= upper_bound)]

# Calculate mean and standard deviation
mean_value2 = filtered_data2['TimeDifference'].mean()
std_deviation2 = filtered_data2['TimeDifference'].std()

# Define Gaussian function
def gaussian(x, amp, mu, sigma):
    return amp * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

# Histogram data
hist, bin_edges = np.histogram(filtered_data['TimeDifference'], bins=range(int(filtered_data['TimeDifference'].min()), 
                  int(filtered_data['TimeDifference'].max()) + 25, 25), density=True)

bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Histogram data
hist2, bin_edges2 = np.histogram(filtered_data2['TimeDifference'], bins=range(int(filtered_data2['TimeDifference'].min()), 
                  int(filtered_data2['TimeDifference'].max()) + 25, 25), density=True)

bin_centers2 = (bin_edges2[:-1] + bin_edges2[1:]) / 2

# Fit Gaussian
popt, pcov = curve_fit(gaussian, bin_centers, hist, p0=[1, mean_value, std_deviation])

# Fit Gaussian
popt2, pcov2 = curve_fit(gaussian, bin_centers2, hist2, p0=[1, mean_value2, std_deviation2])

# Extract the mean and standard deviation of the fitted Gaussian
fitted_amp, fitted_mean, fitted_std = popt

# Extract the mean and standard deviation of the fitted Gaussian
fitted_amp2, fitted_mean2, fitted_std2 = popt2

# Plot the histogram and the fitted Gaussian
plt.figure(figsize=(10, 6))
sns.histplot(filtered_data['TimeDifference'], bins=bin_edges, kde=False, color='#FF8080', stat='density')
plt.axvline(mean_value, color='#800000', linestyle='solid', linewidth=1, label=f'1 Stimulus - Mean: {mean_value:.2f} ms')
plt.axvline(mean_value + std_deviation, color='#FF0000', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation:.2f} ms')
plt.axvline(mean_value - std_deviation, color='#FF0000', linestyle='dashed', linewidth=1)

# Plot Gaussian fit
x_fit = np.linspace(mean_value - 4*std_deviation, mean_value + 4*std_deviation, 1000)
y_fit = gaussian(x_fit, *popt)
plt.plot(x_fit, y_fit, color='#FF0000', linewidth=2, label=f'Gaussian Fit 1 Stimulus: μ = {fitted_mean:.2f} ms, σ = {fitted_std:.2f} ms')

sns.histplot(filtered_data2['TimeDifference'], bins=bin_edges2, kde=False, color='#8080FF', stat='density')
plt.axvline(mean_value2, color='#000080', linestyle='solid', linewidth=1, label=f'2 Stimulus - Mean: {mean_value2:.2f} ms')
plt.axvline(mean_value2 + std_deviation2, color='#0000FF', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation2:.2f} ms')
plt.axvline(mean_value2 - std_deviation2, color='#0000FF', linestyle='dashed', linewidth=1)

x_fit2 = np.linspace(mean_value2 - 4*std_deviation2, mean_value2 + 4*std_deviation2, 1000)
y_fit2 = gaussian(x_fit2, *popt2)
plt.plot(x_fit2, y_fit2, color='#0000FF', linewidth=2, label=f'Gaussian Fit 2 Stimulus: μ = {fitted_mean2:.2f} ms, σ = {fitted_std2:.2f} ms')

# Remove all trials with False in the 'Correct' column
filtered_data3 = data3[data3['Correct'] == True]

# Convert time columns to numeric
filtered_data3['ObjShowTime'] = pd.to_numeric(filtered_data3['ObjShowTime'])
filtered_data3['ReactionTime'] = pd.to_numeric(filtered_data3['ReactionTime'])

# Calculate ReactionTime - ObjShowTime
filtered_data3['TimeDifference'] = filtered_data3['ReactionTime'] - filtered_data3['ObjShowTime']

# Remove 50 ms from all trials
filtered_data3['TimeDifference'] = filtered_data3['TimeDifference'] - 50

# Remove outliers beyond 1.5*IQR
Q1 = filtered_data3['TimeDifference'].quantile(0.25)
Q3 = filtered_data3['TimeDifference'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

filtered_data3 = filtered_data3[(filtered_data3['TimeDifference'] >= lower_bound) & (filtered_data3['TimeDifference'] <= upper_bound)]

# Calculate mean and standard deviation
mean_value3 = filtered_data3['TimeDifference'].mean()
std_deviation3 = filtered_data3['TimeDifference'].std()

# Histogram data
hist3, bin_edges3 = np.histogram(filtered_data3['TimeDifference'], bins=range(int(filtered_data3['TimeDifference'].min()), 
                  int(filtered_data3['TimeDifference'].max()) + 25, 25), density=True)

bin_centers3 = (bin_edges3[:-1] + bin_edges3[1:]) / 2

# Fit Gaussian
popt3, pcov3 = curve_fit(gaussian, bin_centers3, hist3, p0=[1, mean_value3, std_deviation3])

# Extract the mean and standard deviation of the fitted Gaussian
fitted_amp3, fitted_mean3, fitted_std3 = popt3

# Plot the histogram and the fitted Gaussian
sns.histplot(filtered_data3['TimeDifference'], bins=bin_edges3, kde=False, color='#80FF80', stat='density')
plt.axvline(mean_value3, color='#008000', linestyle='solid', linewidth=1, label=f'3 Stimuli - Mean: {mean_value3:.2f} ms')
plt.axvline(mean_value3 + std_deviation3, color='#00FF00', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation3:.2f} ms')
plt.axvline(mean_value3 - std_deviation3, color='#00FF00', linestyle='dashed', linewidth=1)

# Plot Gaussian fit
x_fit3 = np.linspace(mean_value3 - 4*std_deviation3, mean_value3 + 4*std_deviation3, 1000)
y_fit3 = gaussian(x_fit3, *popt3)
plt.plot(x_fit3, y_fit3, color='#00FF00', linewidth=2, label=f'Gaussian Fit 3 Stimuli: μ = {fitted_mean3:.2f} ms, σ = {fitted_std3:.2f} ms')

plt.title('Histogram for Auditory 1, 2, and 3 Stimuli Reflex Time with Gaussian Fit')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 600)
plt.tight_layout()
plt.show()