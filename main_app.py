## Merging all apps in one code
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite, sph_harm
from scipy.constants import hbar, pi
import plotly.graph_objects as go

# Define the individual app functions
def harmonic_oscillator():
    # [Paste the Harmonic Oscillator code here, excluding imports and main()]

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
    

def hydrogen_orbitals():

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
    
    st.title('Interactive Visualization of Two Hydrogen Atoms')

    phase = st.radio("Choose the orbital phase:", ('In-Phase', 'Out-of-Phase'))

# Using the slider to automatically update the plot
    R = st.slider('Separation distance between hydrogen atoms (in a.u.)', 0.1, 5.0, 2.0, on_change=None)

    fig = plot_3d_psi(R, phase)
    st.plotly_chart(fig, use_container_width=True)


def particle_in_a_box():
    # [Paste the Particle in a Box code here, excluding imports and main()]
    # Sidebar for parameter inputs
    st.sidebar.title("Parameters")
    m = st.sidebar.number_input("Mass of Particle (m)", value=1.0, step=0.1)
    l = st.sidebar.number_input("Length of Box (l)", value=1.0, step=0.1)
    n_levels = st.sidebar.slider('Number of Energy Levels', 1, 10, 5)
    
    # Main content
    st.title('Quantum Particle in a Box Visualization')
    
    def wavefunction(n, x, l):
        """Calculate the wavefunction for a given level, position, and box length."""
        return np.sqrt(2 / l) * np.sin(n * pi * x / l)
    
    def energy_level(n, m, l):
        """Calculate the energy level for a given level, mass, and box length."""
        return n**2 * pi**2 * hbar**2 / (2 * m * l**2)
    
    # Plotting code
    fig, ax1 = plt.subplots()
    
    x = np.linspace(0, l, 1000)  # x-values within the box
    
    # Only one axis is needed since we're aligning everything according to energy levels
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Energy / Wave Amplitude')
    
    colors = plt.cm.viridis(np.linspace(0, 1, n_levels))
    
    for n, color in zip(range(1, n_levels + 1), colors):
        psi_n = wavefunction(n, x, l)
        energy = energy_level(n, m, l)
        
        # Normalize wavefunction for visualization purposes
        psi_n_normalized = psi_n / np.max(np.abs(psi_n)) * energy / 10  # Adjust scaling factor as needed
        
        # Offset wavefunction to start at its corresponding energy level
        psi_n_offset = psi_n_normalized + energy
        
        # Plot the energy level as a horizontal line
        ax1.hlines(energy, 0, l, colors='gray', linestyles='dashed', label=f'Energy n={n}' if n == 1 else "")
    
        # Plot wavefunction
        ax1.plot(x, psi_n_offset, label=f'Wavefunction n={n}', color=color)
        
        # Plot probability density (squared wavefunction), also offset
        probability_density_offset = psi_n**2 / np.max(np.abs(psi_n**2)) * energy / 10 + energy  # Adjust scaling
        ax1.fill_between(x, energy, probability_density_offset, color=color, alpha=0.3)
    
    # Adjust layout to make room for the legend
    #ax1.legend()
    ax1.grid(True)
    plt.tight_layout()
    
    st.pyplot(fig)
 

def particle_in_a_box_2d():
    # [Paste the Particle in a Box 2D code here, excluding imports and main()]

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


def rigid_rotor():
    # [Paste the Rigid Rotor code here, excluding imports and main()]


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



def main():
    st.sidebar.title("Quantum Chemistry Visualizations")
    app_option = st.sidebar.radio(
        "Choose the simulation:",
        ('Harmonic Oscillator', 'Hydrogen Orbitals', 'Particle in a Box', 'Particle in a Box 2D', 'Rigid Rotor')
    )

    if app_option == 'Harmonic Oscillator':
        harmonic_oscillator()
    elif app_option == 'Hydrogen Orbitals':
        hydrogen_orbitals()
    elif app_option == 'Particle in a Box':
        particle_in_a_box()
    elif app_option == 'Particle in a Box 2D':
        particle_in_a_box_2d()
    elif app_option == 'Rigid Rotor':
        rigid_rotor()

if __name__ == "__main__":
    main()



