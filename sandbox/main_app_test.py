## Merging all apps in one code
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite, sph_harm
from scipy.constants import hbar, pi
import plotly.graph_objects as go
import math

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
        prefactor = (m * omega / (np.pi * hbar))**(1/4) / np.sqrt(2**n * math.factorial(n))
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

def harmonic_oscillator_2d():
    # Sidebar for parameter inputs
    st.sidebar.title("Parameters")
    m = st.sidebar.number_input("Mass of Particle (m)", value=1.0, step=0.1)
    omega_x = st.sidebar.number_input("Angular frequency in x-direction (ωx)", value=1.0, step=0.1)
    omega_y = st.sidebar.number_input("Angular frequency in y-direction (ωy)", value=1.0, step=0.1)
    nx = st.sidebar.slider('Quantum Number nx', 0, 5, 0)
    ny = st.sidebar.slider('Quantum Number ny', 0, 5, 0)

    # Main content
    st.title('2D Quantum Harmonic Oscillator Visualization')
    
    def wavefunction_2d(nx, ny, x, y, omega_x, omega_y):
        """Calculate the 2D wavefunction for given quantum numbers, positions, and angular frequencies."""
        hermite_x = hermite(nx)
        hermite_y = hermite(ny)
        psi_x = hermite_x(np.sqrt(m * omega_x / hbar) * x) * np.exp(-m * omega_x * x**2 / (2 * hbar))
        psi_y = hermite_y(np.sqrt(m * omega_y / hbar) * y) * np.exp(-m * omega_y * y**2 / (2 * hbar))
        return psi_x * psi_y

    # Grid for plotting
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)

    # Calculate wavefunction for given nx, ny
    psi = wavefunction_2d(nx, ny, X, Y, omega_x, omega_y)

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


def free_particle_1d():
    st.sidebar.title("Parameters")
    k = st.sidebar.number_input("Wave number (k)", value=1.0, step=0.1)
    A = st.sidebar.number_input("Amplitude (A)", value=1.0, step=0.1)
    x_min = st.sidebar.number_input("Minimum x", value=-10.0, step=1.0)
    x_max = st.sidebar.number_input("Maximum x", value=10.0, step=1.0)

    st.title('Quantum Free Particle in 1D')

    def wavefunction_free_particle(x, k, A):
        """Calculate the wavefunction for a free particle."""
        return A * np.exp(1j * k * x)

    x = np.linspace(x_min, x_max, 1000)
    psi = wavefunction_free_particle(x, k, A)

    plt.figure(figsize=(12, 6))
    plt.plot(x, np.real(psi), label='Real part of ψ(x)')
    plt.plot(x, np.imag(psi), label='Imaginary part of ψ(x)', linestyle='dashed')
    plt.plot(x, np.abs(psi), label='|ψ(x)|', linestyle='dotted')
    plt.xlabel("Position (x)")
    plt.ylabel("Wavefunction ψ(x)")
    plt.title("Wavefunction of a Quantum Free Particle in 1D")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def quantum_tunneling():
    st.sidebar.title("Parameters")
    V0 = st.sidebar.number_input("Barrier height (V₀)", value=10.0, step=0.1)
    E = st.sidebar.number_input("Energy of particle (E)", value=5.0, step=0.1)
    a = st.sidebar.number_input("Barrier width (a)", value=2.0, step=0.1)
    x_min = st.sidebar.number_input("Minimum x", value=-10.0, step=1.0)
    x_max = st.sidebar.number_input("Maximum x", value=10.0, step=1.0)

    st.title('Quantum Tunneling Through a Potential Barrier')

    def wavefunction_tunneling(x, V0, E, a):
        """Calculate the wavefunction for quantum tunneling."""
        k1 = np.sqrt(2 * E / hbar**2) if E > 0 else 0
        k2 = np.sqrt(2 * (V0 - E) / hbar**2) if E < V0 else k1

        def psi_left(x):  # Left region (before the barrier)
            return np.exp(1j * k1 * x) + np.exp(-1j * k1 * x)

        def psi_barrier(x):  # Inside the barrier
            return np.exp(-k2 * x) + np.exp(k2 * x)

        def psi_right(x):  # Right region (after the barrier)
            return np.exp(1j * k1 * x)

        psi = np.piecewise(x,
                           [x < -a / 2, (-a / 2 <= x) & (x <= a / 2), x > a / 2],
                           [psi_left, psi_barrier, psi_right])

        return psi

    x = np.linspace(x_min, x_max, 1000)
    psi = wavefunction_tunneling(x, V0, E, a)

    plt.figure(figsize=(12, 6))
    plt.plot(x, np.real(psi), label='Real part of ψ(x)')
    plt.plot(x, np.imag(psi), label='Imaginary part of ψ(x)', linestyle='dashed')
    plt.plot(x, np.abs(psi), label='|ψ(x)|', linestyle='dotted')
    plt.axvline(-a/2, color='red', linestyle='--', label='Barrier start')
    plt.axvline(a/2, color='red', linestyle='--', label='Barrier end')
    plt.xlabel("Position (x)")
    plt.ylabel("Wavefunction ψ(x)")
    plt.title("Wavefunction for Quantum Tunneling")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def particle_in_finite_well():
    st.sidebar.title("Parameters")
    V0 = st.sidebar.number_input("Potential well depth (V₀)", value=10.0, step=0.1)
    L = st.sidebar.number_input("Width of the well (L)", value=2.0, step=0.1)
    E = st.sidebar.number_input("Energy of the particle (E)", value=5.0, step=0.1)
    x_min = st.sidebar.number_input("Minimum x", value=-10.0, step=1.0)
    x_max = st.sidebar.number_input("Maximum x", value=10.0, step=1.0)

    st.title('Particle in a Finite Potential Well')

    def wavefunction_finite_well(x, V0, L, E):
        """Calculate the wavefunction for a particle in a finite potential well."""
        k1 = np.sqrt(2 * E / hbar**2) if E < V0 else 0  # Inside the well
        k2 = np.sqrt(2 * (V0 - E) / hbar**2) if E < V0 else np.sqrt(2 * (E - V0) / hbar**2)  # Outside the well

        def psi_left(x):  # Left region (before the well)
            return np.exp(k2 * x)

        def psi_well(x):  # Inside the well
            return np.sin(k1 * (x + L / 2))

        def psi_right(x):  # Right region (after the well)
            return np.exp(-k2 * x)

        psi = np.piecewise(x,
                           [x < -L / 2, (-L / 2 <= x) & (x <= L / 2), x > L / 2],
                           [psi_left, psi_well, psi_right])

        return psi

    x = np.linspace(x_min, x_max, 1000)
    psi = wavefunction_finite_well(x, V0, L, E)

    plt.figure(figsize=(12, 6))
    plt.plot(x, np.real(psi), label='Real part of ψ(x)')
    plt.plot(x, np.imag(psi), label='Imaginary part of ψ(x)', linestyle='dashed')
    plt.plot(x, np.abs(psi), label='|ψ(x)|', linestyle='dotted')
    plt.axvline(-L/2, color='red', linestyle='--', label='Well boundary start')
    plt.axvline(L/2, color='red', linestyle='--', label='Well boundary end')
    plt.xlabel("Position (x)")
    plt.ylabel("Wavefunction ψ(x)")
    plt.title("Wavefunction for Particle in a Finite Potential Well")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, pi
from scipy.special import factorial
from scipy.integrate import simps

def franck_condon():
    st.sidebar.title("Parameters")
    displacement = st.sidebar.slider("Displacement between ground and excited state potential (Δx)", 0.0, 2.0, 0.5, 0.1)
    n_vib_ground = st.sidebar.slider("Number of vibrational levels in the ground state", 1, 10, 3)
    n_vib_excited = st.sidebar.slider("Number of vibrational levels in the excited state", 1, 10, 3)

    st.title("Franck-Condon Principle and Electronic Transitions")

    # Harmonic oscillator potential function
    def harmonic_potential(x, k):
        return 0.5 * k * x**2

    # Vibrational wavefunction (harmonic oscillator)
    def harmonic_wavefunction(n, x, k, m):
        normalization = (1 / np.sqrt(2**n * factorial(n))) * (m * k / (pi * hbar))**0.25
        hermite_polynomial = np.polynomial.hermite.hermval(np.sqrt(m * k / hbar) * x, [0]*n + [1])
        return normalization * hermite_polynomial * np.exp(-0.5 * m * k * x**2 / hbar)

    # Parameters for the plot
    x = np.linspace(-3, 3, 1000)
    k_ground = 1  # Arbitrary units for the force constant
    m = 1  # Mass (in arbitrary units)
    k_excited = 1  # Assume similar force constant for the excited state

    # Calculate potentials
    V_ground = harmonic_potential(x, k_ground)
    V_excited = harmonic_potential(x - displacement, k_excited)

    # Plot the potential energy curves
    plt.figure(figsize=(10, 6))
    plt.plot(x, V_ground, label='Ground State Potential', color='blue')
    plt.plot(x, V_excited, label='Excited State Potential', color='red')

    # Plot the vibrational levels and wavefunctions
    for n in range(n_vib_ground):
        E_n = (n + 0.5) * hbar * np.sqrt(k_ground / m)
        psi_n = harmonic_wavefunction(n, x, k_ground, m) + E_n
        plt.plot(x, psi_n, color='blue', alpha=0.6)
        plt.hlines(E_n, -3, 3, colors='blue', linestyles='--', alpha=0.5)

    for n in range(n_vib_excited):
        E_n_excited = (n + 0.5) * hbar * np.sqrt(k_excited / m)
        psi_n_excited = harmonic_wavefunction(n, x - displacement, k_excited, m) + E_n_excited
        plt.plot(x, psi_n_excited, color='red', alpha=0.6)
        plt.hlines(E_n_excited, -3, 3, colors='red', linestyles='--', alpha=0.5)

        # Calculate Franck-Condon factors (integral of the overlap between wavefunctions)
        fc_factors = []
        for m_level in range(n_vib_ground):
            psi_m_ground = harmonic_wavefunction(m_level, x, k_ground, m)
            overlap = simps(psi_n_excited * psi_m_ground, x)
            fc_factors.append(overlap**2)

        # Visualize the transitions based on Franck-Condon factors
        for m_level, fc_factor in enumerate(fc_factors):
            if fc_factor > 0.01:  # Only show significant overlaps
                E_m_ground = (m_level + 0.5) * hbar * np.sqrt(k_ground / m)
                plt.plot([x[np.argmax(psi_n_excited)], x[np.argmax(harmonic_wavefunction(m_level, x, k_ground, m))]], 
                         [E_n_excited, E_m_ground], color='green', alpha=fc_factor, linewidth=2*fc_factor)

    plt.title("Franck-Condon Principle: Electronic Transitions in a Molecule")
    plt.xlabel("Position (x)")
    plt.ylabel("Energy")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def main():
    st.sidebar.title("Quantum Chemistry Visualizations")
    st.sidebar.write("beta version")
    app_option = st.sidebar.radio(
        "Choose the simulation:",
        ('Harmonic Oscillator', 'Hydrogen Orbitals', 'Particle in a Box', 'Particle in a Box 2D', 'Rigid Rotor', 
         'Harmonic Oscillator 2D', 'Quantum Free Particle in 1D', 'Quantum Tunneling', 
         'Particle in a Finite Potential Well', 'Molecular Orbitals', 'Vibrational Modes', 
         'Franck-Condon Principle', 'Rotational Spectra', 'Electron Probability Density', 
         'Chemical Bonding', 'Periodic Trends', 'H2+ Molecule Ion')
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
    elif app_option == 'Harmonic Oscillator 2D':
        harmonic_oscillator_2d()
    elif app_option == 'Quantum Free Particle in 1D':
        free_particle_1d()
    elif app_option == 'Quantum Tunneling':
        quantum_tunneling()
    elif app_option == 'Particle in a Finite Potential Well':
        particle_in_finite_well()
    elif app_option == 'Franck-Condon Principle':
        franck_condon()
    # Add the other applications as needed

if __name__ == "__main__":
    main()


