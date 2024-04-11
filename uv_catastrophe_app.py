import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def plancks_law(frequency, temperature):
    """Calculate radiation intensity using Planck's law."""
    h = 6.626e-34  # Planck's constant
    c = 3.0e+8  # Speed of light
    k = 1.38e-23  # Boltzmann's constant
    return (2.0 * h * frequency**3) / (c**2) * 1 / (np.exp((h * frequency) / (k * temperature)) - 1)

def rayleigh_jeans_law(frequency, temperature):
    """Calculate radiation intensity using Rayleigh-Jeans Law."""
    c = 3.0e+8  # Speed of light
    k = 1.38e-23  # Boltzmann's constant
    return (2 * np.pi * frequency**2 * k * temperature) / c**2

st.title("UV Catastrophe & Planck's Solution")

temperature = st.slider("Temperature (K)", min_value=500, max_value=5000, value=1500, step=100)

frequency = np.linspace(1e12, 1e15, 500)  # Frequency range from 1 THz to 1000 THz

planck_intensity = plancks_law(frequency, temperature)
rj_intensity = rayleigh_jeans_law(frequency, temperature)

fig, ax = plt.subplots()
ax.plot(frequency, planck_intensity, label="Planck's Law")
ax.plot(frequency, rj_intensity, label="Rayleigh-Jeans Law", linestyle='--')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Intensity')
ax.set_title(f'Black Body Radiation at {temperature}K')
ax.legend()

st.pyplot(fig)

