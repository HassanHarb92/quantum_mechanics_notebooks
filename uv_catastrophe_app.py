import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 3e8  # Speed of light in meters per second
h = 6.626e-34  # Planck constant in J*s
k_B = 1.38e-23  # Boltzmann constant in J/K

def rayleigh_jeans(lamb, T):
    """Rayleigh-Jeans Law"""
    return (2 * c * k_B * T) / (lamb**4)

def planck(lamb, T):
    """Planck's Law"""
    exponent = (h * c) / (lamb * k_B * T)
    return (2 * h * c**2) / (lamb**5) / (np.exp(exponent) - 1)

def plot_radiation(T):
    # Wavelength range (in meters)
    lambda_min, lambda_max = 1e-9, 3e-6  # from 1 nm to 3000 nm
    wavelengths = np.linspace(lambda_min, lambda_max, 400)
    
    # Calculate intensities
    intensities_rj = rayleigh_jeans(wavelengths, T)
    intensities_p = planck(wavelengths, T)
    
    # Create plot
    fig, ax = plt.subplots()
    ax.plot(wavelengths, intensities_rj, label='Rayleigh-Jeans')
    ax.plot(wavelengths, intensities_p, label='Planck')
    ax.set_xlabel('Wavelength (m)')
    ax.set_ylabel('Intensity (W/m^3)')
    ax.set_title(f'Blackbody Radiation at T = {T} K')
    ax.legend()
    
    return fig

# Streamlit interface
st.title("Simulation of the UV Catastrophe")
T = st.slider("Select Temperature (K)", 1000, 10000, 5000)
fig = plot_radiation(T)
st.pyplot(fig)

