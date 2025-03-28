
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Separation Zone Visualization Tool", layout="centered")
st.title("Separation Zone Visualization Tool")

# Sidebar inputs
st.sidebar.header("Adjust Parameters")

r1 = st.sidebar.number_input("Light Phase Weir Radius (r₁) [m]", min_value=0.001, max_value=0.5, value=0.10, step=0.001, format="%.3f")
r2 = st.sidebar.number_input("Heavy Phase Weir Radius (r₂) [m]", min_value=0.001, max_value=0.5, value=0.15, step=0.001, format="%.3f")
r_channel = st.sidebar.number_input("Rising Channel Radius [m]", min_value=0.001, max_value=0.5, value=0.05, step=0.001, format="%.3f")
rho1 = st.sidebar.number_input("Light Phase Density (ρ₁) [kg/m³]", min_value=600.0, max_value=1200.0, value=850.0, step=0.1, format="%.1f")
rho2 = st.sidebar.number_input("Heavy Phase Density (ρ₂) [kg/m³]", min_value=800.0, max_value=1400.0, value=1000.0, step=0.1, format="%.1f")
bowl_radius = st.sidebar.number_input("Bowl Inner Radius (m)", min_value=0.001, max_value=0.5, value=0.22, step=0.001, format="%.3f")

# Calculate interface radius R
if rho1 != rho2:
    R_squared = (rho1 * r1**2 - rho2 * r2**2) / (rho1 - rho2)
    R = np.sqrt(R_squared) if R_squared > 0 else None
else:
    R = None

# Plotting
fig, ax = plt.subplots(figsize=(6, 2.5))

if R and R < bowl_radius:
    st.metric(label="Interface Radius (R)", value=f"{R:.4f} m")

    # Yellow from 0 to R
    ax.barh(y=0.5, width=R, left=0, height=1, color='yellow', edgecolor='black', label='Light Phase')
    # Blue from R to bowl_radius
    ax.barh(y=0.5, width=bowl_radius - R, left=R, height=1, color='blue', edgecolor='black', label='Heavy Phase')

    # Weir and channel indicators
    ax.axvline(r1, color='green', linestyle='-', linewidth=2, label='r₁ (Light Weir)')
    ax.axvline(r2, color='blue', linestyle='-', linewidth=2, label='r₂ (Heavy Weir)')
    ax.axvline(r_channel, color='purple', linestyle='--', linewidth=2, label='Rising Channel')
else:
    st.warning("Cannot compute interface position (R): check inputs or ensure it is less than the bowl radius.")
    # Show full blue if R invalid
    ax.barh(y=0.5, width=bowl_radius, left=0, height=1, color='blue', edgecolor='black', label='Heavy Phase')

    # Weir and channel indicators
    ax.axvline(r1, color='green', linestyle='-', linewidth=2, label='r₁ (Light Weir)')
    ax.axvline(r2, color='blue', linestyle='-', linewidth=2, label='r₂ (Heavy Weir)')
    ax.axvline(r_channel, color='purple', linestyle='--', linewidth=2, label='Rising Channel')

# Style and labels
ax.set_xlim(0, bowl_radius)
ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xticks(np.round(np.linspace(0, bowl_radius, 9), 3))
ax.set_xlabel("Radius (m)")
ax.set_title("Interface and Features Across Bowl Radius")
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=3)
ax.grid(True, axis='x')

st.pyplot(fig)
