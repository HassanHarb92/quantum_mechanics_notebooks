import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Constants
a0 = 1.0  # Bohr radius in arbitrary units

def psi_1s(r):
    """Calculate the wavefunction of 1s orbital."""
    return np.pi**-0.5 * np.exp(-r/a0)

def plot_3d_psi(R):
    # Create a denser grid
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    z = np.linspace(-5, 5, 100)
    X, Y, Z = np.meshgrid(x, y, z)
    
    # Positions of the two hydrogen atoms
    R1 = np.sqrt((X + R/2)**2 + Y**2 + Z**2)  # Hydrogen 1
    R2 = np.sqrt((X - R/2)**2 + Y**2 + Z**2)  # Hydrogen 2

    # Calculate wavefunction for both atoms and sum them
    Psi = psi_1s(R1)**2 + psi_1s(R2)**2

    # Selecting a higher threshold for visualization
    threshold = Psi.max()/20
    xs, ys, zs = X[Psi > threshold], Y[Psi > threshold], Z[Psi > threshold]
    values = Psi[Psi > threshold]

    # Create a 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(x=xs.flatten(), y=ys.flatten(), z=zs.flatten(),
                                       mode='markers',
                                       marker=dict(size=2,
                                                   color=values.flatten(),
                                                   colorscale='Blues',
                                                   opacity=0.5))])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(aspectmode='cube'))

    return fig

# Streamlit app setup
st.title('Interaction Visualization of Two Hydrogen Atoms')

# Slider for adjusting the separation distance
R = st.slider('Separation distance between hydrogen atoms (in a.u.)', 0.1, 5.0, 2.0)

if st.button('Plot Ψ for Two Hydrogens'):
    fig = plot_3d_psi(R)
    st.plotly_chart(fig, use_container_width=True)

