import streamlit as st
import importlib.util

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

# Function to load module with caching
@st.cache_resource #()#(allow_output_mutation=True)
def load_module(app_path):
    try:
        spec = importlib.util.spec_from_file_location("module.name", app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        st.write(f"Module {app_path} loaded successfully.")
        return module
    except Exception as e:
        st.error(f"Failed to load module {app_path}: {e}")
        return None



# Dropdown to select the app
selected_app = st.radio("Select an app to run:", list(apps.keys()))

# Check if the current app has changed or needs to be loaded
if 'current_app' not in st.session_state or st.session_state.current_app != selected_app:
    st.session_state.module = load_module(apps[selected_app])
    st.session_state.current_app = selected_app

# Button to run the app
if st.button("Run App"):
    # Execute the main function of the app
    if hasattr(st.session_state.module, 'main'):
        st.session_state.module.main()
    else:
        st.error("No main function found in the selected app!")


## still not working .. need to fix issue with app reloading
