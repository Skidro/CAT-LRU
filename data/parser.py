import os
import re
import pylab as pl


# Declare the file name
workingSet = 5120
partitionSize = '7_5mb'
fileName = str(workingSet) + '_' + partitionSize + '_swap.log'

# Verify that the file exists in the current directory
if not os.path.isfile(os.getcwd() + '/' + fileName):
	raise IOError, 'File %s not found!' % (fileName)

# Create dictionary for storing parsed data
data = {}
data['IPC-1'] = []
data['IPC-2'] = []
data['MISS-1'] = []
data['MISS-2'] = []

# Define regex for different kind of lines in the data file
timeRegex = "^TIME \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
part1Regex = "^[ ]*0-1[ ]*([\d\.]*)[ ]*([\dk]*)[ ]*([\d\.]*)$"
part2Regex = "^[ ]*2-11[ ]*([\d\.]*)[ ]*([\dk]*)[ ]*([\d\.]*)$"

# Variables for tracking time stamps
migrationStep = 24
currentStep = 0

# Parse file
with open(fileName, 'r') as fdi:
	lines = fdi.readlines()

	for line in lines:
		# Try to math the line against partition-1 regex
		linePartition_1 = re.match(part1Regex, line)

		if linePartition_1:
			# Store partition-1 data
			data['IPC-1'].append(float(linePartition_1.group(1)))
			data['MISS-1'].append(int(linePartition_1.group(2)[:-1]))
		else:
			# Try to math the line against partition-2 regex
			linePartition_2 = re.match(part2Regex, line)
			
			if linePartition_2:
				# Store partition-1 data
				data['IPC-2'].append(float(linePartition_2.group(1)))
				data['MISS-2'].append(int(linePartition_2.group(2)[:-1]))

		# Keep track of the time steps
		if re.match(timeRegex, line):
			currentStep += 1

			if (currentStep == migrationStep):
				# Swap regex rules
				temp = part1Regex
				part1Regex = part2Regex
				part2Regex = temp


def plot_data(fig_name, title, x_axis, data_1, data_2, x_title, y_title):
	max_y = max(max(data_1), max(data_2))
	min_y = min(min(data_1), min(data_2))
	range_y = max_y - min_y
	
	# Leave a margin of 5% at top and bottom
	y_axis_upper_bound = max_y + 0.05 * range_y
	y_axis_lower_bound = min_y - 0.05 * range_y
	
	# Create a canvas for drawing the plot
	fig = pl.figure(figsize = (15, 15))

	# Draw the plots
	pl.plot(x_axis[:43], data_1[:43], 'b', marker = '^', label = 'Mild')
	pl.plot(x_axis[22:], data_2[22:], 'r', marker = 'o', label = 'Intensive')
	pl.plot([22, 22], [y_axis_upper_bound, y_axis_lower_bound], 'k--', label = 'Mild-Starts - Intensive Migrates')
	pl.plot([42, 42], [y_axis_upper_bound, y_axis_lower_bound], 'g--', label = 'Intensive Ends')
	pl.ylim(y_axis_lower_bound, y_axis_upper_bound)
	pl.xlim(0, x_axis[-1])
	pl.title(title)
	pl.xlabel(x_title)
	pl.ylabel(y_title)

	# Place a legend on the upper right corner of the plot
	pl.legend(loc = 'upper left', shadow = True)

	# Save the figure with the given name
	fig.savefig(fig_name)

# Plot the data
x_axis = range(0, len(data['IPC-1']))

# Plot the IPC data
plot_data('ipc.jpg', 'Instructions per Cycle (IPC)', x_axis, data['IPC-1'], data['IPC-2'], 'Time (seconds)', 'IPC')

# Plot the LLC Miss data
scaled_miss_1 = [x * 1000 for x in data['MISS-1']]
scaled_miss_2 = [x * 1000 for x in data['MISS-2']]
plot_data('miss.jpg', 'LLC Misses', x_axis, scaled_miss_1, scaled_miss_2, 'Time (seconds)', 'Number of Misses')
