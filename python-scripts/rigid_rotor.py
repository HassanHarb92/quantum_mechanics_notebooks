import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm

def plot_wavefunction(J, M):
    # Ensure M is within the valid range
    M = max(-J, min(J, M))

    # Angles
    theta, phi = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]

    # Spherical harmonics
    Y = sph_harm(M, J, theta, phi)

    # Cartesian coordinates
    r = np.abs(Y)
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)
    st.pyplot(fig)

# Streamlit UI
st.title('Rigid Rotor Wavefunctions')

# Slider for J
J = st.slider('J:', 0, 5, 0)

# Slider for M
M = st.slider('M:', -J, J, 0)

# Plotting button (optional, you can just call the plot function directly)
if st.button('Plot Wavefunction'):
    plot_wavefunction(J, M)
else:
    # Default plot or message
    st.write('Use the sliders to adjust J and M, then press "Plot Wavefunction".')

# Save this script as `streamlit_app.py` and run it using the command `streamlit run streamlit_app.py` in your terminal.

