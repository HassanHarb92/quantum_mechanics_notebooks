import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
a0 = 1.0  # Bohr radius in arbitrary units

def psi_1s(r):
    """Calculate the wavefunction of 1s orbital."""
    return np.pi**-0.5 * np.exp(-r/a0)

def plot_3d_psi():
    # Create a grid
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    z = np.linspace(-5, 5, 100)
    X, Y, Z = np.meshgrid(x, y, z)
    R = np.sqrt(X**2 + Y**2 + Z**2)

    # Calculate wavefunction
    Psi = psi_1s(R)

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # We plot the square of the wavefunction to represent probability density
    # Use a threshold to avoid cluttering the plot with low-probability regions
    ax.scatter(X[Psi > 0.1], Y[Psi > 0.1], Z[Psi > 0.1], color='blue', s=1)
    ax.set_box_aspect([1,1,1])  # Aspect ratio is 1:1:1

    return fig

# Streamlit app
st.title('Visualization of the 1s Orbital of a Hydrogen Atom')

if st.button('Plot Ψ₁ₛ'):
    fig = plot_3d_psi()
    st.pyplot(fig)

