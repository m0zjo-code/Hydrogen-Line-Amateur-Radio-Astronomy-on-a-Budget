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
__date__ = "01/05/2019"
__maintainer__ = "Jonathan/M0ZJO"
__status__ = "Development"

# Import libs
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import time, sys, getopt, os
from datetime import datetime

# Import AstroPy 
from astropy.coordinates import SkyCoord, EarthLocation
from astropy import units as u

# Data output settings
plot = False
plot_noise = False
export_fig = False
calc_doppler = False
calc_velocity = False

# Rx location
lat = 51
lon = 0.5
height = 100

# Constants
h_cf = 1420.40575e6
c = 2.9979246e8

# Function to calculate a gradient to equalise the two vectors
# y = m * x -> m is calculated iteratively
def equalise_power(vec1, vec2):
    var = 1
    stop = 0.000001
    cv = 2
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
        var = var+cv*e

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
    # Load arguments
    help_line = "hlineprocess.py -d <datafile> -n <noisefile> -l <fft_len> -p <az,el>"
    try:
        opts, args = getopt.getopt(argv,"d:n:l:p:h",['data=', 'noise=', 'fftlen=', 'pointing=', 'help'])
    except getopt.GetoptError:
        print("Options error:")
        print(help_line)
        sys.exit(1)
    # Verify argument    
    if len(opts) == 0:
        print("Please run with the following options:")
        print(help_line)
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print(help_line)
            sys.exit()
        elif opt in ("-d"):
            datafile = arg
        elif opt in ("-n"):
            noisefile = arg
        elif opt in ("-l"):
            fft_len = int(arg)
        elif opt in ("-p"):
            pointing = arg.split(",")
    
    # Display system info
    print_header()
    print("### Data file: ", datafile)
    print("### Noise file: ", noisefile)
    print("### fft_len is:", fft_len)
    
    # Define receiver location
    home = EarthLocation.from_geodetic(lat, lon, height)
    
    # Generate output location
    if export_fig:
        # Get output info
        output_str = input("Please enter the output folder name: ")
        
        # Test if folder exists
        # From: https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
        try:
            os.makedirs(output_str)
        except FileExistsError:
            # Directory already exists
            pass
    
    # Load noise grid
    noise, noise_measurement_time = read_file(noisefile, fft_len)
    # Discard f values
    noise_vector = noise[:,:,1]
    # Sum values
    noise_vector = np.sum(noise_vector, axis = 0)/noise_vector.shape[0]
    
    # Load antenna data
    data_block, data_measurement_time = read_file(datafile, fft_len)
    print("### %i records found\n" % data_block.shape[0])
    
    # Iterate over data tracks
    for i in range(0, data_block.shape[0]):
        # Extract data block
        block = data_block[i, :, :]
        
        # Calculate correction
        correction = equalise_power(block[:,1], noise_vector)
        
        # Apply amplitude correction
        plot_data = block[:,1]- noise_vector*correction
        plot_data = np.square(plot_data)
        
        # Generate time string
        time_str = data_measurement_time[i].strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate default plot labels
        xlabel = "Frequency/Hz"
        ylabel = "Power Counts"
        plot_title = ("Hydrogen Line Measurement - %s\nHawkhurst, UK\nAz:%s El:%s" % (time_str, pointing[0], pointing[1]))
        
        # Perform Doppler calculations
        if calc_doppler:
            block[:,0] = block[:,0] - h_cf
            xlabel = "Doppler Offset/Hz"
        elif calc_velocity:
            block[:,0] = (block[:,0] - h_cf)*c/h_cf
            xlabel = "Relative Velocity/ m/s"
        
        # Cast Alt Az values
        alt = float(pointing[0])*u.deg
        az = float(pointing[1])*u.deg
        
        # Get block info
        AltAzcoordiantes = SkyCoord(alt = alt, az = az, obstime = time_str, frame = 'altaz', location = home)
        
        # Display measurement info
        print("### %s, %s, %s" % (time_str, AltAzcoordiantes.icrs.ra, AltAzcoordiantes.icrs.dec))
        
        # Display data
        if plot:
            # Plot data
            plt.title(plot_title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.plot(block[:,0], plot_data)
            plt.show()
        
        # Display noise data (corrected)
        if plot_noise:
            plt.plot(block[:,0], block[:,1])
            plt.plot(block[:,0], noise_vector*correction)
            plt.show()
        
        # Export figure to disk (PNG)
        if export_fig:
            plt.title(plot_title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.plot(block[:,0], plot_data)
            plt.savefig("%s/%s_%i.png" % (output_str, output_str, i), bbox_inches='tight')
            plt.close()
        
# Print info about the software
def print_header():
    name = """
###############################
 __  __  ___ _____   _  ___  
|  \/  |/ _ \__  /  | |/ _ \ 
| |\/| | | | |/ /_  | | | | |
| |  | | |_| / /| |_| | |_| |
|_|  |_|\___/____\___/ \___/ 
###############################
"""
    print(name)
    print("### hlineprocess.py version %s release date %s ###" % (__version__, __date__))
    print("### Written by %s. Happy Beeping! ###\n\n" % __author__)

if __name__ == "__main__":
    main(sys.argv[1:])