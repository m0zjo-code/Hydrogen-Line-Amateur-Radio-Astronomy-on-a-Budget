#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#File        read_h_line_data.py
#Author      Jonathan Rawlinson/M0ZJO
#Date        26/04/2019
#Desc.       This is a script to read data from rtl_power_fftw 
#            written by Klemen Blokar and Andrej Lajovic.
#            https://github.com/AD-Vega/rtl-power-fftw
#            The input file and noise reference are read, equalised and 
#            subtracted to output the spectral output

# Import libs
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import time

# Function to calculate a gradient to equalise the two vectors
# y = m * x -> m is calculated iteratively
def equalise_power(vec1, vec2):
    var = 1
    stop = 0.00001
    c = 2
    e = float("inf")
    while True:
        e_old = e
        e = np.sum(vec1 - vec2*var)
        #print(e, var, abs(e) - abs(e_old))
        if abs(e - e_old) < stop:
            return var
        var = var+c*e

# Function to read rtl_power_fftw output file
def read_file(filename, no_bins):
    f = open(filename, "r")
    data_block = []
    while True:
        x = f.readline()
        if len(x) == 0:
            break
        if x == "# rtl-power-fftw output\n":
            #print("Data Found")
            start_line = f.readline()
            end_line = f.readline()
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
    f.close()
    return np.array(data_block)

noise = read_file("../21042019_Data/NoiseD1.dat", 1024)
noise_vector = noise[:,:,1]
noise_vector = np.sum(noise_vector, axis = 0)/noise_vector.shape[0]

data_block = read_file("../21042019_Data/MeasD1Az315El70a_120k.dat", 1024)

for block in data_block:
    correction = equalise_power(block[:,1], noise_vector)
    
    plot_data = block[:,1]- noise_vector*correction
    plot_data = np.square(plot_data)
    
    #plt.plot(block[:,0], block[:,1])
    #plt.plot(block[:,0], noise_vector*correction)
    #plt.show()
    
    plt.title("Hydrogen Line Measurement - 21/04/2019\nHawkhurst, UK")
    plt.xlabel("Frequency/Hz")
    plt.ylabel("Power Counts")  
    plt.plot(block[:,0], plot_data)
    plt.show()