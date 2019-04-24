import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import time


def equalise_power(vec1, vec2):
    var = 1
    offset = 0.001
    stop = 0.0016
    while True:
        val0 = np.sum(np.abs(vec1 - vec2*(var-offset)))
        val1 = np.sum(np.abs(vec1 - vec2*var))
        val2 = np.sum(np.abs(vec1 - vec2*(var+offset)))
        print(var, val0, val1, val2)
        
        if val1 < stop:
            return var
        
        if val0<val2:
            var -= offset
        else:
            var += offset
        
        


no_bins= 1024

f = open("../21042019_Data/NoiseD1.dat", "r")
noise = []
while True:
    x = f.readline()
    if len(x) == 0:
        break
    if x == "# rtl-power-fftw output\n":
        print("Data Found")
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
        noise.append(data_list)
    
f.close()

noise = np.array(noise)

noise_vector = noise[:,:,1]
print(noise_vector.shape)
noise_vector = np.sum(noise_vector, axis = 0)/noise_vector.shape[0]
print(noise_vector.shape)

ctr = 0
f = open("../21042019_Data/MeasD1Az315El70a_120k.dat", "r")

while True:
    x = f.readline()
    if len(x) == 0:
        break
    if x == "# rtl-power-fftw output\n":
        print("Data Found")
        ctr = ctr + 1
        print(ctr)
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
        data_list = np.array(data_list)
        print(data_list.shape)
        
        correction = equalise_power(data_list[:,1], noise_vector)
        
        plot_data = data_list[:,1]- noise_vector*correction
        plot_data = np.square(plot_data)*1e10
        
        b, a = butter(20, 0.3, btype = 'low', analog = False)
        
        #plot_data = filtfilt(b, a, plot_data)
        plt.plot(data_list[:,0], data_list[:,1])
        plt.plot(data_list[:,0], noise_vector*correction)
        plt.show()
        
        plt.title("Hydrogen Line Measurement - 21/04/2019\nHawkhurst, UK. Az:046 El:71\n2019-04-21 11:41:49 UTC - 2019-04-21 11:42:10 UTC")
        plt.xlabel("Frequency/Hz")
        plt.ylabel("Power Counts")  
        plt.plot(data_list[:,0], plot_data)
        
        #plt.plot(data_list[:,0], data_list[:,1])
        #plt.plot(data_list[:,0], noise_vector*1.9)
        plt.autoscale()
        #plt.savefig("out/%i.png" % ctr)
        #plt.close()
        plt.show()
    
f.close()
