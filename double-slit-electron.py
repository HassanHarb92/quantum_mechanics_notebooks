import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('Double-Slit Experiment Model')

# Choices
wave_type = st.radio("Choose the wave type:", ('Light', 'Electron'))
num_slits = st.slider('Number of slits', 2, 5, 2)

# Wave-specific parameters
if wave_type == 'Light':
    wavelength = st.slider('Wavelength (nm)', 380, 750, 550)  # Visible light spectrum
elif wave_type == 'Electron':
    wavelength = st.slider('Wavelength (pm)', 10.0, 50.0, 12.3, 0.1)  # Typical electron wavelength with float parameters

distance_between_slits = st.slider('Distance between slits (micrometers)', 1, 100, 50)
distance_to_screen = st.slider('Distance to screen (meters)', 1, 10, 2)
slit_width = st.slider('Slit width (micrometers)', 10, 500, 200)

# Constants
pi = np.pi

# Calculation for multi-slit interference
y = np.linspace(-0.01, 0.01, 400)
beta = pi * slit_width * 1e-6 * y / (wavelength * 1e-9 * distance_to_screen)
intensity = (np.sin(beta) / beta)**2
for i in range(1, num_slits):
    intensity *= (np.cos(pi * i * distance_between_slits * 1e-6 * y / (wavelength * 1e-9 * distance_to_screen)))**2

# Plot
fig, ax = plt.subplots()
ax.plot(y, intensity, color='blue')
ax.set_xlabel('Position on screen (m)')
ax.set_ylabel('Intensity')
st.pyplot(fig)

