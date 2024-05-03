import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# Constants
c = 3e8  # Speed of light in meters per second
h = 6.626e-34  # Planck constant in J*s
k_B = 1.38e-23  # Boltzmann constant in J/K

def planck(lamb, T):
    """Planck's Law"""
    exponent = (h * c) / (lamb * k_B * T)
    return (2 * h * c**2) / (lamb**5) / (np.exp(exponent) - 1)

def plot_radiation(max_lambda, T):
    # Wavelength range (in meters)
    lambda_min = 1e-9  # minimum wavelength is 1 nm
    wavelengths = np.linspace(lambda_min, max_lambda, 500)
    
    fig, ax = plt.subplots()
    intensity = planck(wavelengths, T)
    ax.plot(wavelengths*1e9, intensity, label=f'{T} K', color='blue')  # Convert wavelength to nanometers

    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Intensity (W/m^3)')
    ax.set_title(f'Blackbody Radiation at {T} K')
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, max_lambda*1e9)  # Adjust x-axis limit to slider value
    ax.set_ylim(0, 1.5e13)  # Adjust y-axis for better visualization
    
    return fig

# Streamlit interface
st.title("Simulation of Blackbody Radiation")
T = st.slider("Select Temperature (K)", 300, 10000, 5000, step=100)
max_lambda_nm = st.slider("Select Maximum Wavelength (nm)", 10, 3000, 2000)  # Slider in nm
fig = plot_radiation(max_lambda_nm * 1e-9, T)  # Convert nm to m
st.pyplot(fig)

