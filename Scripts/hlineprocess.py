#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#File        hlineprocess.py
#Author      Jonathan Rawlinson/M0ZJO
#Date        27/04/2019
#Desc.       This is a script to read data from rtl_power_fftw 
#            written by Klemen Blokar and Andrej Lajovic.
#            https://github.com/AD-Vega/rtl-power-fftw
#            The input file and noise reference are read, equalised and 
#            subtracted to output the spectral output

__author__ = "Jonathan/M0ZJO"
__copyright__ = "Jonathan/M0ZJO 2019"
__credits__ = ["https://github.com/AD-Vega/rtl-power-fftw"]
__license__ = "MIT"
__version__ = "0.0.1"
__date__ = "27/04/2019"
__maintainer__ = "Jonathan/M0ZJO"
__status__ = "Development"

# Import libs
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import time, sys, getopt
from datetime import datetime

# Function to calculate a gradient to equalise the two vectors
# y = m * x -> m is calculated iteratively
def equalise_power(vec1, vec2):
    var = 1
    stop = 0.000001
    c = 2
    e = float("inf")
    while True:
        # Store old error
        e_old = e
        # Calculate new error
        e = np.sum(vec1 - vec2*var)
        # Test to see if error has improved enough since previous iteration
        if abs(e - e_old) < stop:
            return var
        # Apply new gradient value
        var = var+c*e

# Function to read rtl_power_fftw output file
def read_file(filename, no_bins):
    # Open data file
    f = open(filename, "r")
    data_block = []
    timestamps = []
    # Loop over file
    while True:
        # Read line
        x = f.readline()
        if len(x) == 0:
            break
        if x == "# rtl-power-fftw output\n":
            #print("Data Found")
            start_line = f.readline()
            start_line = start_line.split(" ")
            # # Acquisition start: 2019-04-21 10:48:42 UTC
            start_time = datetime.strptime(start_line[3] + " " + start_line[4], "%Y-%m-%d %H:%M:%S")
            
            end_line = f.readline()
            end_line = end_line.split(" ")
            # # Acquisition end: 2019-04-21 10:49:03 UTC
            end_time = datetime.strptime(end_line[3] + " " + end_line[4], "%Y-%m-%d %H:%M:%S")
            mid_time = (end_time - start_time)/2 + start_time
            empty_line = f.readline()
            units = f.readline()
            data_list = []
            for i in range(0, no_bins):
                j = f.readline()
                j = j[:-1]
                j_s = j.split(" ")
                j_s[0] = float(j_s[0])
                j_s[1] = float(j_s[1])
                data_list.append(j_s)
            data_block.append(data_list)
            timestamps.append(mid_time)
    f.close()
    return np.array(data_block), timestamps


def main(argv):
    cf = 1420.40575e6 
    
    # Load arguments
    try:
        opts, args = getopt.getopt(argv,"hd:n:l:",["ifile=","fft_len="])
    except getopt.GetoptError:
        print("Options error:")
        print('hlineprocess.py -d <datafile> -n <noisefile> -l <fft_len>')
        sys.exit(2)
    # Verify argument    
    if len(opts) == 0:
        print("Please run with the following options:")
        print('hlineprocess.py -d <datafile> -n <noisefile> -l <fft_len>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('hlineprocess.py -d <datafile> -n <noisefile> -l <fft_len>')
            sys.exit()
        elif opt in ("-d", "--ifile_data"):
            datafile = arg
        elif opt in ("-n", "--ifile_noise"):
            noisefile = arg
        elif opt in ("-l", "--fftlen"):
            fft_len = int(arg)
    
    print_header()
    print("### Data file: ", datafile)
    print("### Noise file: ", noisefile)
    print("### fft_len is:", fft_len)
    
    # Load noise grid
    noise, noise_measurement_time = read_file(noisefile, fft_len)
    # Discard f values
    noise_vector = noise[:,:,1]
    # Sum values
    noise_vector = np.sum(noise_vector, axis = 0)/noise_vector.shape[0]
    
    # Load antenna data
    data_block, data_measurement_time = read_file(datafile, fft_len)
    print(data_measurement_time) 
    
    # Iterate over data tracks
    for block in data_block:
        # Calculate correction
        correction = equalise_power(block[:,1], noise_vector)
        
        # Apply correction
        plot_data = block[:,1]- noise_vector*correction
        plot_data = np.square(plot_data)
        
        #plt.plot(block[:,0], block[:,1])
        #plt.plot(block[:,0], noise_vector*correction)
        #plt.show()
        
        # Plot data
        plt.title("Hydrogen Line Measurement - 21/04/2019\nHawkhurst, UK")
        plt.xlabel("Frequency/Hz")
        plt.ylabel("Power Counts")  
        plt.plot(block[:,0], plot_data)
        plt.show()

# Print info about the software
def print_header():
    name = """
###############################
 __  __  ___ _____   _  ___  
|  \/  |/ _ \__  /  | |/ _ \ 
| |\/| | | | |/ /_  | | | | |
| |  | | |_| / /| |_| | |_| |
|_|  |_|\___/____\___/ \___/ 
"""
    print(name)
    print("### hlineprocess.py version %s release date %s ###" % (__version__, __date__))
    print("### Written by %s. Happy Beeping! ###\n\n" % __author__)

if __name__ == "__main__":
    main(sys.argv[1:])
