import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite


def main():

    # Streamlit interface for user inputs
    st.title("Quantum Harmonic Oscillator Visualization")
    m = st.sidebar.number_input("Mass of the particle (m)", value=1.0, step=0.1)
    omega = st.sidebar.number_input("Angular frequency (ω)", value=1.0, step=0.1)
    n_levels = st.sidebar.slider("Number of energy levels", 1, 10, 5)
    hbar = 1
    # Quantum harmonic oscillator potential function
    def potential(x):
        return 0.5 * m * omega**2 * x**2
    
    # Energy level function
    def energy_level(n):
        return (n + 0.5) * hbar * omega
    
    # Wavefunction
    def wavefunction(n, x):
        prefactor = (m * omega / (np.pi * hbar))**(1/4) / np.sqrt(2**n * np.math.factorial(n))
        hermite_poly = hermite(n)
        return prefactor * hermite_poly((m * omega / hbar)**0.5 * x) * np.exp(-m * omega * x**2 / (2 * hbar))
    
    # Preparing the plot
    x = np.linspace(-5, 5, 1000)  # Range of x values
    plt.figure(figsize=(12, 8))
    
    # Plotting the potential
    plt.plot(x, potential(x), label="Potential", color='black')
    plt.title("Potential and Wavefunctions for a Quantum Harmonic Oscillator")
    plt.xlabel("Position (x)")
    plt.ylabel("Energy / Amplitude")
    
    # Plotting the energy levels and wavefunctions
    for n in range(n_levels):
        energy_n = energy_level(n)
        plt.hlines(energy_n, x[0], x[-1], colors='grey', linestyles='--', label=f"Energy level {n}" if n == 0 else "")
        plt.plot(x, wavefunction(n, x) + energy_n, label=f"Wavefunction n={n}")
    
    plt.ylim(0, energy_level(n_levels) + 1)
    plt.legend()
    plt.grid(True)
    
    # Display the plot in the Streamlit app
    st.pyplot(plt)
    

if __name__ == "__main__":
    main()


