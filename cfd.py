#!/usr/bin/env python
#
# CFD Calculation
# ===============
#
# Simulation of flow in a 2D box using the Jacobi algorithm.
#

import sys
import time

# Import the external jacobi function from "jacobi.py"
from jacobi import jacobi

def main(argv):

    # Test we have the correct number of arguments
    if len(argv) < 2:
        print "Usage: cfd.py <scalefactor> <iterations>"
        sys.exit(1)
    
    # Get the systen parameters from the arguments
    scalefactor = int(sys.argv[1])
    niter = int(sys.argv[2])
    
    sys.stdout.write("\n2D CFD Simulation\n")
    sys.stdout.write("=================\n")
    sys.stdout.write("Scale Factor = {0}\n".format(scalefactor))
    sys.stdout.write("  Iterations = {0}\n".format(niter))

    # Time the initialisation
    tstart = time.time()
    
    # Set the parameters for boundry conditions
    b = 5*scalefactor 
    h = 15*scalefactor
    w = 5*scalefactor 

    # Set the dimensions of the array
    m = 32*scalefactor
    n = 32*scalefactor
    
    # Define the psi array and set it to zero
    psi = [[0 for col in range(m+2)] for row in range(n+2)]
    
    # Set the bondary conditions on bottom edge
    for i in range(b+1, b+w):
        psi[0][i] = float(i-b)
    for i in range(b+w, m+1):
        psi[0][i] = float(w)
    # Set the bondary conditions on right edge
    for j in range(1, h+1):
        psi[j][m+1] = float(w)
    for j in range(h+1, h+w):
        psi[j][m+1] = float(w-j+h)
    
    # Write the simulation details
    tend = time.time()
    sys.stdout.write("\nInitialisation took {0:.5f}s\n".format(tend-tstart))
    sys.stdout.write("\nGrid size = {0} x {1}\n".format(m, n))
    
    # Call the Jacobi iterative loop (and calculate timings)
    sys.stdout.write("\nStarting main Jacobi loop...\n")
    tstart = time.time()
    jacobi(niter, psi)
    tend = time.time()
    sys.stdout.write("...finished\n")
    sys.stdout.write("\nCalculation took {0:.5f}s\n\n".format(tend-tstart))
    
    # Write the output file
    write_data(m, n, psi, "flow.dat")

    # Finish nicely
    sys.exit(0)

# Create a plot of the data using matplotlib
def write_data(m, n, psi, outfile):

    # Open the specified file
    out = open(outfile, "w")
    out.write("{0} {1}\n".format(m, n))
    # Loop over stream function matric (without boundaries)
    for i in range(1, m+1):
        for j in range(1, n+1):
            # Compute velocities and magnitude squared
            xvel = (psi[i][j+1] - psi[i][j-1])/2.0
            yvel = (psi[i-1][j] - psi[i+1][j])/2.0
            mvs = (xvel + yvel)**2
            # Scale the magnitude
            modvsq = mvs**0.3
            out.write("{0:5d} {1:5d} {2:10.5f} {3:10.5f} {4:10.5f}\n".format(i-1, j-1, xvel, yvel, modvsq))
    out.close()

# Function to create tidy way to have main method
if __name__ == "__main__":
        main(sys.argv[1:])

