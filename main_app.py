import streamlit as st
import importlib.util
import sys

st.title("Quantum chemistry interactive apps")
st.markdown("Select app from drop-down menu")
st.markdown("beta version")

# List of apps
apps = {
    "Hydrogen Orbital": "Hydrogen_orbital.py",
    "Harmonic Oscillator": "harmonic_oscillator.py",
    "Particle in a Box": "particle_in_a_box.py",
    "Particle in a Box 2D": "particle_in_a_box_2D.py",
    "Rigid Rotor": "rigid_rotor.py"
}

# Dropdown to select the app
selected_app = st.selectbox("Select an app to run:", list(apps.keys()))

# Button to run the app
if st.button("Run App"):
    # Get the file of the selected app
    app_path = apps[selected_app]

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("module.name", app_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Execute the main function of the app, if you follow this pattern in your sub-apps
    if hasattr(module, 'main'):
        module.main()
    else:
        st.error("No main function found in the selected app!")

