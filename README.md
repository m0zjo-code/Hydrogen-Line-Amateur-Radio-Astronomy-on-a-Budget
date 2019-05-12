
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


## Antenna Simulations and Design
[Yagicad](http://www.yagicad.com/yagicad/YagiCAD.htm) was used to design a 1 meter yagi antenna that responded well at 1420 MHz. This antenna came out to have 16 elements and have the response below:![Antenna Pattern](/AntennaV1Data/AntennaPattern.PNG)
The antenna has the following physical layout as shown below and the element design parameters are shown [in this PDF](/AntennaV1Data/CuOvereview.pdf). The YC6 (for use with YagiCad) file is available [here](/AntennaV1Data/DL6WU20_HLINEV1Cu.YC6) if you would like to play with the design yourself.

![Antenna Physical Layout](/AntennaV1Data/AntennaPlot.PNG)

## Filter Information
The amplifier used in the initial test was the "VBFZ-1400-S+" from Mini-Circuits.
Webpage: https://www.minicircuits.com/WebStore/dashboard.html?model=VBFZ-1400-S%2B
Datasheet: https://ww2.minicircuits.com/pdfs/VBFZ-1400+.pdf

This filter is a major cost in this project. In the future I hope to design a micro strip filter to provide a lower cost alternative.

## Low Noise Amplifier Info
- S measurements
- Circuit?

## SDR Info 

## Results
- Discuss results
- Interference

## Processing tool (dark frame processing and antenna pointing assistance)
- Antenna pointing assistance
- Noise subtraction
- Plot data on galactic plane (fits?)

## Next steps
- Raspberry pi recorder
- HackRF (using soapy power)
- Filter
