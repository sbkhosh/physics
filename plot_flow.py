#!/usr/bin/env python
#
# Plot the output from Jacobi CFD calculation
#

# Import the required functions
import numpy as np
import sys

def main(argv):

    # Input and output files
    infile = argv[0]
    outfile = argv[1]

    # Open the input file
    input = open(infile, "r")

    # Read the dimensions of the simulation
    line = input.readline()
    line = line.rstrip()
    tokens = line.split()
    m = int(tokens[0])
    n = int(tokens[1])

    # Define and zero the numpy arrays
    modvsq = np.zeros((m, n))
    xvel = np.zeros((m, n))
    yvel = np.zeros((m, n))

    # Loop over the grid reading the data into the arrays
    for i in range(1, m+1):
        for j in range(1, n+1):
            
            line = input.readline()
            line = line.rstrip()
            tokens = line.split()
            i1 = int(tokens[0])
            j1 = int(tokens[1])
            xvel[i1,j1] = float(tokens[2])
            yvel[i1,j1] = float(tokens[3])
            modvsq[i1,j1] = float(tokens[4])
    input.close()


    # Plot a heatmap overlayed with velocity streams
    import matplotlib

    # Plot to image file without need for X server
    matplotlib.rcParams['font.size'] = 8
    matplotlib.use("Agg")

    # Import the required functions
    from matplotlib import pyplot as plt
    from matplotlib import cm

    fig = plt.figure()

    # Regular grids
    x = np.linspace(0, m-1, m)
    y = np.linspace(0, n-1, n)

    # Line widths are scaled by modulus of velocity
    lw = 3 * modvsq/modvsq.max()

    # Create the stream lines denoting the velocities
    plt.streamplot(x, y, xvel, yvel, color='k', density=1.5, linewidth=lw)

    # Create the heatmap denoting the modulus of the velocities
    plt.imshow(modvsq, interpolation='nearest', cmap=cm.jet)

    # Save the figure to the output PNG file
    fig.savefig(outfile)

if __name__ == "__main__":
        main(sys.argv[1:])
