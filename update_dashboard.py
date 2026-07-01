import streamlit as st
import pandas as pd

# 1. Sidebar Setup & Explanation Mode Toggle
st.sidebar.header("Configuration")
show_explanation = st.sidebar.toggle("ℹ️ Enable Health Informatics Explanation Mode", value=True)

# 2. Dynamic Column Mapping Inputs based on Mode
st.sidebar.subheader("Column mapping")
if show_explanation:
    st.sidebar.caption("Define how your incoming telemetry columns correspond to clinical biomechanics standards.")

timestamp_col = st.sidebar.text_input(
    "Timestamp column", 
    value="timestamp",
    help="**Temporal Anchor:** Syncs data with EHR systems or patient logs." if show_explanation else None
)

accel_x_col = st.sidebar.text_input(
    "X-axis column", 
    value="accel_x",
    help="**Medio-Lateral (ML) Axis:** Measures side-to-side sway; critical for fall-risk assessments." if show_explanation else None
)

accel_y_col = st.sidebar.text_input(
    "Y-axis column", 
    value="accel_y",
    help="**Vertical (V) Axis:** Measures up-and-down motion; essential for calculating step impacts and gait velocity." if show_explanation else None
)

accel_z_col = st.sidebar.text_input(
    "Z-axis column", 
    value="accel_z",
    help="**Antero-Posterior (AP) Axis:** Measures forward-and-backward motion; key for detecting forward trips or sudden acceleration changes." if show_explanation else None
)

# 3. Main Dashboard Layout
st.title("Stream Ingestion Dashboard")
st.subheader("SKDH Stream Viewer")

# Health Informatics Educational Banner
if show_explanation:
    with st.expander("💡 Health Informatics Deep Dive: Clinical Validation with SKDH", expanded=True):
        st.markdown("""
        **Scikit-Digital-Health (SKDH)** is an open-source framework used to turn high-frequency, noisy wearable sensor data (from devices like Apple Watch, Fitbit, ActiGraph) into validated **digital clinical biomarkers**.
        
        **How the mapped data is utilized:**
        * **Ingestion & Normalization:** Your custom column inputs are mapped to standard Cartesian vectors.
        * **Resampling & Filtering:** Signal noise is reduced, and frequencies are normalized to standard windows (e.g., 100Hz).
        * **Biomarker Extraction:** SKDH processes these raw streams into endpoints such as **gait asymmetry, rest-activity cycles, sleep latency, and physical activity intensity profiles** for clinical trials.
        """)

# File Uploader
uploaded_file = st.file_uploader(
    "Upload CSV or JSON telemetry", 
    type=["csv", "json"],
    help="Upload a file to automatically normalize its contents into SKDH-compatible structures."
)

if uploaded_file is not None:
    st.success("File uploaded successfully! Ready for mapping validation.")
else:
    st.info("Upload a CSV or JSON file to begin. The dashboard will normalize the payload into SKDH-compatible time/acceleration arrays.")
