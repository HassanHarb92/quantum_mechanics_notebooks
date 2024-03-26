import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Constants
a0 = 1.0  # Bohr radius in arbitrary units

def psi_1s(r):
    """Calculate the wavefunction of 1s orbital."""
    return (np.pi**-0.5) * np.exp(-r/a0)

def plot_3d_psi(R, phase):
    # Grid setup
    x = np.linspace(-5, 5, 50)  # Reduced for performance in surface plot
    y = np.linspace(-5, 5, 50)
    z = np.linspace(-5, 5, 50)
    X, Y, Z = np.meshgrid(x, y, z)
    
    # Positions of the two hydrogen atoms
    R1 = np.sqrt((X + R/2)**2 + Y**2 + Z**2)  # Hydrogen 1
    R2 = np.sqrt((X - R/2)**2 + Y**2 + Z**2)  # Hydrogen 2

    # Calculate wavefunction for both atoms
    if phase == 'In-Phase':
        Psi = psi_1s(R1)**2 + psi_1s(R2)**2
    else:  # Out-of-Phase
        Psi = np.abs(psi_1s(R1)**2 - psi_1s(R2)**2)  # Absolute value to visualize the density

    # Visualization threshold for the isosurface
    threshold = Psi.max()/10  # Adjust if needed for clearer visualization

    # Create a 3D isosurface plot
    fig = go.Figure(data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=Psi.flatten(),
        isomin=threshold,
        isomax=Psi.max(),
        surface=dict(count=3, fill=0.7),  # Adjust for surface detail and transparency
        caps=dict(x_show=False, y_show=False, z_show=False),
        colorscale='Blues',
        opacity=0.6  # Adjust for desired transparency
    ))

    # Update plot layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(aspectmode='cube'))

    return fig

# Streamlit app setup
st.title('Interactive Visualization of Two Hydrogen Atoms')

phase = st.radio("Choose the orbital phase:", ('In-Phase', 'Out-of-Phase'))

# Using the slider to automatically update the plot
R = st.slider('Separation distance between hydrogen atoms (in a.u.)', 0.1, 5.0, 2.0, on_change=None)

fig = plot_3d_psi(R, phase)
st.plotly_chart(fig, use_container_width=True)

