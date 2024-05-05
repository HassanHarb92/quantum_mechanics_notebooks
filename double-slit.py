import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('Double-Slit Experiment Model')

# User Inputs
wavelength = st.slider('Wavelength (nm)', 400, 700, 550)
distance_between_slits = st.slider('Distance between slits (micrometers)', 1, 100, 50)
distance_to_screen = st.slider('Distance to screen (meters)', 1, 10, 2)
slit_width = st.slider('Slit width (micrometers)', 10, 500, 200)

# Constants
pi = np.pi

# Calculation
y = np.linspace(-0.01, 0.01, 400)
beta = pi * slit_width * 1e-6 * y / (wavelength * 1e-9 * distance_to_screen)
intensity = (np.sin(beta) / beta)**2 * (np.cos(pi * distance_between_slits * 1e-6 * y / (wavelength * 1e-9 * distance_to_screen)))**2

# Plot
fig, ax = plt.subplots()
ax.plot(y, intensity, color='blue')
ax.set_xlabel('Position on screen (m)')
ax.set_ylabel('Intensity')
st.pyplot(fig)


