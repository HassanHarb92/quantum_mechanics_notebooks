import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Constants
a0 = 1.0  # Bohr radius in arbitrary units

def psi_1s(r):
    """Calculate the wavefunction of 1s orbital."""
    return np.pi**-0.5 * np.exp(-r/a0)

def plot_3d_psi():
    # Create a grid
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    z = np.linspace(-3, 3, 50)
    X, Y, Z = np.meshgrid(x, y, z)
    R = np.sqrt(X**2 + Y**2 + Z**2)

    # Calculate wavefunction
    Psi = psi_1s(R)**2  # Plotting the probability density

    # Selecting a threshold for visualization
    threshold = Psi.max()/10
    # Extract the coordinates and values that meet the threshold
    xs, ys, zs = X[Psi > threshold], Y[Psi > threshold], Z[Psi > threshold]
    values = Psi[Psi > threshold]

    # Create a 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(x=xs.flatten(), y=ys.flatten(), z=zs.flatten(),
                                       mode='markers',
                                       marker=dict(size=2,
                                                   color=values.flatten(),  # Set color to probability density
                                                   colorscale='Blues',     # Use a blue color scale
                                                   opacity=0.5))])
    # Update plot layout for a better visual
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(aspectmode='cube'))

    return fig

# Streamlit app
st.title('Interactive Visualization of the 1s Orbital of a Hydrogen Atom')

if st.button('Plot Ψ₁ₛ'):
    fig = plot_3d_psi()
    st.plotly_chart(fig, use_container_width=True)

