import glob

def read_rmsd_file(file_path):
    times = []
    rmsd_values = []

    with open(file_path, 'r') as f:
        for line in f:
            if not line.startswith(('#', '@')):  # Skip comment lines
                parts = line.split()
                time = float(parts[0])
                rmsd = float(parts[1])
                times.append(time)
                rmsd_values.append(rmsd)
    return times, rmsd_values

def calculate_average_rmsd(files_pattern):
    time_rmsd_dict = {}
    count_dict = {}

    # Loop through all files matching the pattern
    for file in glob.glob(files_pattern):
        times, rmsd_values = read_rmsd_file(file)
        for time, rmsd in zip(times, rmsd_values):
            if time not in time_rmsd_dict:
                time_rmsd_dict[time] = rmsd
                count_dict[time] = 1
            else:
                time_rmsd_dict[time] += rmsd
                count_dict[time] += 1

    # Calculate averages
    average_rmsd = {time: time_rmsd_dict[time] / count_dict[time] for time in time_rmsd_dict}

    return average_rmsd

def save_average_rmsd_to_file(output_file, average_rmsd):
    with open(output_file, 'w') as f:
        f.write('# Time and average RMSD values\n')
        f.write('@    title "Average RMSD"\n')
        f.write('@    xaxis  label "Time (ps)"\n')
        f.write('@    yaxis  label "RMSD (nm)"\n')
        f.write('@TYPE xy\n')
        for time, avg_rmsd in sorted(average_rmsd.items()):
            f.write(f'{time:.6f}    {avg_rmsd:.6f}\n')

# Usage example:
files_pattern = '03_equil_set*/equil_npt/rmsd_ref_crystal.xvg' # Adjust the path and file pattern as needed
average_rmsd = calculate_average_rmsd(files_pattern)

# Save the result to an output file
output_file = 'average_rmsd.xvg'  # Change this to your desired output file name
save_average_rmsd_to_file(output_file, average_rmsd)

print(f'Results saved to {output_file}')
