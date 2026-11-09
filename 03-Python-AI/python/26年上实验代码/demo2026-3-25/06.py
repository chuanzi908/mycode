import numpy as np
import matplotlib.pyplot as matplotlib

x=np.arange([0,1,2,3,4,5])
y=np.array([0.1,0.9,2.1,2.9,4.2,5.0])

coeffs=np.polyfit(x,y,deg=2)
p=np.polyld(coeffs)

x_smooth=np.linspace(0,5,100)
matplotlib.scatter(x,y,label='data');matplotlib.plot(x_smooth,p(x_smooth),label='r-')
matplotlib.legend();matplotlib.show()