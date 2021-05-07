import sys
import csv
from mpl_toolkits import mplot3d
import numpy as np 
import matplotlib.pyplot as plt

csvFile = sys.argv[1]
x_points = []
y_points = []
z_points = []
color_points = []
heat_points  = []
clip_distance = 15

def calculateHeatValues(count):
    global heat_points
    heat_points = np.sqrt((x_points - np.mean(x_points))**2 + (y_points - np.mean(y_points))**2 + (z_points - np.mean(z_points))**2)
    heat_points /= np.max(heat_points)

def getDatPoints(fname):
    global x_points
    global y_points
    global z_points
    global color_points
    total_lines = sum(1 for line in open(fname)) - 1
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # These are the header names
                line_count += 1
            elif line_count < total_lines:
                color_points.append(line_count)
                # Add these valus to an array
                x_points.append(float(row[2]))
                y_points.append(float(row[3]))
                z_points.append(float(row[4]))
                line_count += 1
    x_points = np.array(x_points)
    y_points = np.array(y_points)
    z_points = np.array(z_points)
    color_points = np.array(color_points)
    filter_arr = np.logical_and(np.abs(x_points) < clip_distance, np.abs(y_points) < clip_distance, np.abs(z_points) < clip_distance)
    x_points = x_points[filter_arr]
    y_points = y_points[filter_arr]
    z_points = z_points[filter_arr]
    color_points = color_points[filter_arr]
    calculateHeatValues(line_count - 1)
    

def main(fname):

    getDatPoints(fname)

    fig = plt.figure(figsize=plt.figaspect(0.5))

    ax = fig.add_subplot(1, 3, 1, projection='3d')
    # Note that Unity "up (y)" is different from the graph's up NOTE: add colour map
    ax.scatter3D(x_points, z_points, y_points, c = color_points, cmap = 'rainbow')
    ax.set_title('3D point timemap')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Z coordinate')
    ax.set_zlabel('Y coordinate')

    ax = fig.add_subplot(1, 3, 2, projection='3d')
    ax.plot3D(x_points, z_points, y_points, c = 'purple')
    # ax.scatter3D(x_points, z_points, y_points, c = color_points, cmap = 'rainbow')
    ax.set_title('3D point linemap')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Z coordinate')
    ax.set_zlabel('Y coordinate')

    ax = fig.add_subplot(1, 3, 3, projection='3d')
    invert_heat = 1 - heat_points
    ax.scatter3D(x_points, z_points, y_points, c = invert_heat, cmap = 'inferno')
    ax.set_title('3D point heatmap')
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Z coordinate')
    ax.set_zlabel('Y coordinate')

    # Purple shows initial glance and rainbows outwards
    plt.show()

if __name__ == '__main__':
    main(csvFile)
