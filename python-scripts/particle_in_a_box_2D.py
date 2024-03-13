import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.constants import hbar, pi

# Sidebar for parameter inputs
st.sidebar.title("Parameters")
m = st.sidebar.number_input("Mass of Particle (m)", value=1.0, step=0.1)
Lx = st.sidebar.number_input("Length of Box in x-direction (Lx)", value=1.0, step=0.1)
Ly = st.sidebar.number_input("Length of Box in y-direction (Ly)", value=1.0, step=0.1)
nx = st.sidebar.slider('Quantum Number nx', 1, 10, 1)
ny = st.sidebar.slider('Quantum Number ny', 1, 10, 1)

# Main content
st.title('3D Visualization of 2D Quantum Particle in a Box')

def wavefunction(nx, ny, x, y, Lx, Ly):
    """Calculate the 2D wavefunction for given quantum numbers, positions, and box dimensions."""
    return np.sqrt(4 / (Lx * Ly)) * np.sin(nx * pi * x / Lx) * np.sin(ny * pi * y / Ly)

# Grid for plotting
x = np.linspace(0, Lx, 100)
y = np.linspace(0, Ly, 100)
X, Y = np.meshgrid(x, y)

# Calculate wavefunction for given nx, ny
psi = wavefunction(nx, ny, X, Y, Lx, Ly)

# Plotting
fig = go.Figure(data=[go.Surface(z=psi, x=X, y=Y, colorscale='Viridis')])

fig.update_layout(title=f'Wavefunction for nx={nx}, ny={ny}', autosize=True,
                  scene=dict(
                      xaxis_title='X',
                      yaxis_title='Y',
                      zaxis_title='Wave Amplitude',
                      aspectratio=dict(x=1, y=1, z=0.5)),
                  )

st.plotly_chart(fig, use_container_width=True)

