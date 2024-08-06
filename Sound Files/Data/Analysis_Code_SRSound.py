import pandas as pd
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

file_path = '/Users/taneeshkondapally/Downloads/Taneesh_SRrtData_2024-07-23.csv' #INSERT FILE NAME TO ANALYZE HERE
data = pd.read_csv(file_path)

# Remove all trials with False in the 'Correct' column
filtered_data = data[data['Correct'] == True]

# Convert time columns to numeric
filtered_data['ObjShowTime'] = pd.to_numeric(filtered_data['ObjShowTime'])
filtered_data['ReactionTime'] = pd.to_numeric(filtered_data['ReactionTime'])

# Calculate ReactionTime - ObjShowTime
filtered_data['TimeDifference'] = filtered_data['ReactionTime'] - filtered_data['ObjShowTime']

# Convert from seconds to milliseconds
filtered_data['TimeDifference'] = filtered_data['TimeDifference'] * 1000

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

# Define Gaussian function
def gaussian(x, amp, mu, sigma):
    return amp * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

# Histogram data
hist, bin_edges = np.histogram(filtered_data['TimeDifference'], bins=range(int(filtered_data['TimeDifference'].min()), 
                  int(filtered_data['TimeDifference'].max()) + 25, 25), density=True)

bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Fit Gaussian
popt, pcov = curve_fit(gaussian, bin_centers, hist, p0=[1, mean_value, std_deviation])

# Extract the mean and standard deviation of the fitted Gaussian
fitted_amp, fitted_mean, fitted_std = popt

# Output mean and standard deviation
print(f"Mean: {mean_value:.2f} ms")
print(f"Standard Deviation: {std_deviation:.2f} ms")

# Output mean and standard deviation of the fitted Gaussian
print(f"Fitted Gaussian Mean: {fitted_mean:.2f} ms")
print(f"Fitted Gaussian Standard Deviation: {fitted_std:.2f} ms")

# Plot the histogram and the fitted Gaussian
plt.figure(figsize=(10, 6))
sns.histplot(filtered_data['TimeDifference'], bins=bin_edges, kde=False, color='#FF8080', stat='density')
plt.axvline(mean_value, color='#800000', linestyle='solid', linewidth=1, label=f'Mean: {mean_value:.2f} ms')
plt.axvline(mean_value + std_deviation, color='#FF0000', linestyle='dashed', linewidth=1, label=f'Standard Deviation: {std_deviation:.2f} ms')
plt.axvline(mean_value - std_deviation, color='#FF0000', linestyle='dashed', linewidth=1)

# Plot Gaussian fit
x_fit = np.linspace(mean_value - 4*std_deviation, mean_value + 4*std_deviation, 1000)
y_fit = gaussian(x_fit, *popt)
plt.plot(x_fit, y_fit, color='#FF0000', linewidth=2, label=f'Gaussian Fit: μ = {fitted_mean:.2f} ms, σ = {fitted_std:.2f} ms')

plt.title('Histogram for Auditory Simple Reflex Reaction Time with Gaussian Fit')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency Density')
plt.legend()
plt.grid(False)
plt.xlim(0, 600)
plt.show()
