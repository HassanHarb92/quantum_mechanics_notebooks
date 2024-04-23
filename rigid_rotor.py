import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.special import sph_harm

def main():

    def plot_wavefunction_with_plotly(J, M):
        # Ensure M is within the valid range
        M = max(-J, min(J, M))
    
        # Angles
        phi, theta = np.mgrid[0:np.pi:50j, 0:2*np.pi:100j]
    
        # Spherical harmonics
        Y = sph_harm(M, J, theta, phi)
    
        # Cartesian coordinates
        r = np.abs(Y)
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
    
        # Create the plot
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis')])
    
        # Update layout for a better view
        fig.update_layout(title=f'Wavefunction for l = {J}, m = {M}', autosize=True,
                          scene=dict(
                              xaxis_title='X',
                              yaxis_title='Y',
                              zaxis_title='Z',
                              xaxis=dict(nticks=4, range=[-0.5,0.5]),
                              yaxis=dict(nticks=4, range=[-0.5,0.5]),
                              zaxis=dict(nticks=4, range=[-0.5,0.5]),
                          ),
                          margin=dict(l=65, r=50, b=65, t=90))
        st.plotly_chart(fig, use_container_width=True)
    
    # Streamlit UI
    st.title('Interactive Rigid Rotor Wavefunctions with Plotly')
    
    # Slider for J
    J = st.slider('l:', 0, 5, 0)
    
    # Conditionally set M slider's range
    if J == 0:
        # Set M's range to only 0 when J is 0
        M = 0
        st.markdown("One m value allowed: 0")
    #    M = st.slider('M:', 0, 0, 0)
    else:
        # Adjusting M slider based on J
        M_min, M_max = -J, J
        M = st.slider('M:', M_min, M_max, 0)
    
    # Plotting with Plotly for interactivity
    plot_wavefunction_with_plotly(J, M)

if __name__ == "__main__":
    main()


