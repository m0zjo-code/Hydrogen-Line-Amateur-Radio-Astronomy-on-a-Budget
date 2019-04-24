from astropy.coordinates import SkyCoord, EarthLocation
from astropy import coordinates as coord
from astropy.coordinates.tests.utils import randomly_sample_sphere
from astropy.time import Time
from astropy import units as u
import numpy as np

import matplotlib.pyplot as plt 

coos = SkyCoord.from_name('M1') 

# 300 times over the space of 10 hours
times = Time.now() + np.linspace(-5, 5, 300)*u.hour

# note the use of broadcasting so that 300 times are broadcast against 1000 positions
lapalma = EarthLocation.from_geodetic(51.023, 0.31)
aa_frame = coord.AltAz(obstime=times[:, np.newaxis], location=lapalma)

# calculate alt-az of each object at each time.
aa_coos = coos.transform_to(aa_frame)  

plt.scatter(aa_coos.az, aa_coos.alt)
plt.show()
