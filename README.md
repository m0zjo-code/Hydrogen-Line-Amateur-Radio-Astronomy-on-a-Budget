

# Hydrogen Line Amateur Radio Astronomy on a Budget
This is an overview of my H-line amateur radio astronomy experiments for others to see.

This work was inspired from the amazing examples provided by Peter East here:
http://y1pwe.co.uk/RAProgs/index.html

I wanted to re-create this work, although unfortunately I live very close to a rail station so needed to modify the setup to be more portable to I could do this "out and about". Also - I'm tight on budget and wanted to see if I could relax the setup requirements to reduce the cost.

## The Hydrogen Line
A great explanation of the hydrogen line can be seen at the link below by HyperPhysics:
http://hyperphysics.phy-astr.gsu.edu/hbase/quantum/h21.html
https://en.wikipedia.org/wiki/Hydrogen_line

TL;DR, Neutral hydrogen emits a carrier at 1.420405GHz. We can use this to calculate the relative velocity of galactic hydrogen clouds using the Doppler effect.  

## The System

![SystemDiagram](/docs/RadioTelescopeSystemDiagram.png)

Photo of the system in action:
![Full System Image](/docs/FullSystem.jpg)

## Antenna Simulations and Design
[Yagicad](http://www.yagicad.com/yagicad/YagiCAD.htm) was used to design a 1 meter yagi antenna that responded well at 1420 MHz. This antenna came out to have 16 elements and have the response below:![Antenna Pattern](/AntennaV1Data/AntennaPattern.PNG)
The antenna has the following physical layout as shown below and the element design parameters are shown [in this PDF](/AntennaV1Data/CuOvereview.pdf). The YC6 (for use with YagiCad) file is available [here](/AntennaV1Data/DL6WU20_HLINEV1Cu.YC6) if you would like to play with the design yourself.

![Antenna Physical Layout](/AntennaV1Data/AntennaPlot.PNG)

## Filter Information
The amplifier used in the initial test was the "VBFZ-1400-S+" from Mini-Circuits.
Webpage: https://www.minicircuits.com/WebStore/dashboard.html?model=VBFZ-1400-S%2B

Datasheet: https://ww2.minicircuits.com/pdfs/VBFZ-1400+.pdf

![Filter Photo](/docs/MiniCircuitsFilter.jpg)

This filter is a major cost in this project. In the future I hope to design a micro strip filter to provide a lower cost alternative.

## (LNA) Low Noise Amplifier Info
Two types of LNAs were purchased for this project, both using the SPF5189Z chip. The front two amplifiers were the "exposed board" type purchased from eBay and the driver amplifier after the filter was purchased from "rtl-sdr.com". The driver LNA is powered via the coax cable and the antenna side amplifiers are powered over separate power inputs. 

These amplifiers claim to work between 50-4000 MHz and have a NF of 0.6dB. They are also very cheap (exposed board from eBay ~£6 GBP and the rtl-sdr.com version ~$17.95 USD)

Exposed Board Amplifier:
![Exposed Board Amplifier Image](/docs/FilterA.jpg)

Post Filter Driver Amplifier:
![Driver Amplifier Image](/docs/FilterB.jpg)

### Example links of where to purchase these amplifiers are below:
- https://www.ebay.co.uk/itm/LNA-50-4000-MHz-RF-Low-Noise-Amplifier-Signal-Receiver-SPF5189-NF-0-6dB-inm-KW/264028670208
- https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/

## SDR Info 
The SDR (Software Defined Radio) used for this work is the "RTL-SDR Blog V3 R820T2 RTL2832U 1PPM TCXO SMA Software Defined Radio" sold at rtl-sdr.com. I have found that this is one of the better RTL dongles and it has a few extra features that some of the cheaper dongles do not have:
- Expansion ports to allow further hacking
- Bias Tee for powering LNAs
- Built in direct sampling for HF

RTL-SDR Blog V3 R820T2 RTL2832U 1PPM TCXO SMA Software Defined Radio Image:
![SDR Image](/docs/RTL.jpg)

## Recording Software
The recording software used for this project was "rtl-power-fftw" by AD-Vega. This is an improved version of "rtl-power" that records wideband power spectral density plots from RTL dongles. The output data is saved in a text file that is then processed further, an example of the output data is shown below:
```
# rtl-power-fftw output
# Acquisition start: 2019-04-21 12:18:07 UTC
# Acquisition end: 2019-04-21 12:19:10 UTC
#
# frequency [Hz] power spectral density [dB/Hz]
1.41940575e+09 2.19498e-05
1.41940771e+09 2.19627e-05
1.41940966e+09 2.14898e-05
1.41941161e+09 2.13466e-05
1.41941356e+09 2.1464e-05
``` 

Link to rtl-power-fftw:
https://github.com/AD-Vega/rtl-power-fftw

### Measurement Process
Two sets of measurements are taken for each observation
- Antenna data
-- This is the measurement that contains the "actual" data from the galaxy. In this mode the antenna is pointed towards the area of interest and data is recorded
- Noise data
-- This is the "dark frame" of the data. The RTL dongles have a pretty poor amplitude response over the input frequency band so a noise frame is required to account for this. Here, a 50 Ohm load is used instead of the antenna so that a "clean" noise measurement can be recorded.

It is important to note that both measurements use the same recording settings.

## Processing tool (dark frame processing and antenna pointing assistance) 
The python 3.x processing script "hlineprocess" is located in the Scripts folder of this repository.

The following libraries are required:
- matplotlib
- numpy
- scipy
- astropy
- healpy

The following functions are provided:
- Parse data files from rtl_power_fftw 
- Antenna pointing assistance
- Noise subtraction
- Plot data locations on the galactic plane (using a 408 MHz allsky map kindly provided by the Jodrell Bank Centre for Astrophysics - http://www.jb.man.ac.uk/research/cosmos/haslam_map/)

The processing script can be used as follows:
``` bash
hlineprocess.py -d <datafile> -n <noisefile> -l <fft_len> -p <el,az>
```` 
Where:
- datafile = filepath of data file
- noisefile = filepath of noise measurement
- fft_len = fft_len used in rtl_power_fftw
- el,az = elevation and azimuth of antenna (used for pointing calculations)

For example:
``` bash
python3 hlineprocess.py -d ../21042019_Data/MeasD1Az315El70a_120k.dat -n ../21042019_Data/NoiseD150ohterm.dat  -l 1024 -p 70,315
```` 

The output methods can be controlled using the variables at the start of the file:
```python
# Data output settings
plot = True # Plot corrected plot
plot_noise = False # Plot noise and raw data
export_fig = False # Export corrected data as a png file
calc_doppler = False # Convert frequency to doppler shift
calc_velocity = True # Convert doppler to velocity
plot_allsky = True # Plot data points on allsky map when file parsing has completed
```

The location of the receive antenna must also be specified:
```python
# Rx location
lat = 51.6
lon = 0.3
height = 100
```

## Results
A number of test recordings were made over a weekend and the results are shown below.

A corrected H-Line response is shown below:
![Example Hline Response](/docs/PlotExample_arm.png)

An example raw data file plot is shown below along with the associated noise measurement. The H-Line response on the blue line can be seen but is dwarfed by the front end response of the SDR (orange line).
![Example Raw Response](/docs/NoiseRaw.png)

More example snapshot results:
![Example H-Line Response](/21042019_Data/MeasD1Az282El45/MeasD1Az282El45-2.png)

![Example H-Line Response](/21042019_Data/MeasD1Az312El77/MeasD1Az312El77.png)

Unfortunately, not much data was recorded when the setup was available but enough was recorded to prove that the setup is functional.

## Next steps
- Raspberry pi recorder
- HackRF (using soapy power)
- Filter
