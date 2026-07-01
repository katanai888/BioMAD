import streamlit as st
import pandas as pd

# Page Configuration for a wider, professional layout
st.set_page_config(page_title="BioMAD & SKDH Ingestion Pipeline", layout="wide")

# ==========================================
# 1. SIDEBAR CONFIGURATION & CLINICAL MAPPING
# ==========================================
st.sidebar.header("📋 Stream Configuration")

# The Core Toggle for Health Informatics Mode
show_explanation = st.sidebar.toggle("ℹ️ Enable Health Informatics Explanation Mode", value=True)

st.sidebar.write("---")
st.sidebar.subheader("Axis & Temporal Mapping")

if show_explanation:
    st.sidebar.caption(
        "Map incoming device-specific telemetry to standardized clinical biomechanics axes "
        "required for physical endpoint calculations."
    )
else:
    st.sidebar.caption("Map custom payload keys to target system axes.")

# Interactive inputs with dynamic, education-focused tooltips
timestamp_col = st.sidebar.text_input(
    "Timestamp column", 
    value="timestamp",
    help=(
        "**Temporal Anchor:** Synchronizes raw streaming sensor windows with objective external events "
        "(e.g., electronic patient-reported outcomes [ePROs], controlled clinical trial logs, or EHR timestamps)."
    ) if show_explanation else "The key for your datetime array."
)

accel_x_col = st.sidebar.text_input(
    "X-axis column", 
    value="accel_x",
    help=(
        "**Medio-Lateral (ML) Axis:** Captures coronal-plane, side-to-side acceleration vectors. "
        "Critical for calculating lateral sway, postural instability, and fall-risk indices in neurodegenerative profiles."
    ) if show_explanation else "Raw acceleration vector on the X-axis."
)

accel_y_col = st.sidebar.text_input(
    "Y-axis column", 
    value="accel_y",
    help=(
        "**Vertical (V) Axis:** Captures longitudinal, superior-inferior acceleration. "
        "The primary vector utilized for calculating step-impact forces, heel-strike velocity, and gait cadence."
    ) if show_explanation else "Raw acceleration vector on the Y-axis."
)

accel_z_col = st.sidebar.text_input(
    "Z-axis column", 
    value="accel_z",
    help=(
        "**Antero-Posterior (AP) Axis:** Captures sagittal-plane, forward-and-backward acceleration vectors. "
        "Essential for analyzing forward translational velocity, propulsion, and catching sudden forward trips or stumbles."
    ) if show_explanation else "Raw acceleration vector on the Z-axis."
)

# ==========================================
# 2. MAIN DASHBOARD CONTENT
# ==========================================
st.title("Stream Ingestion Dashboard")
st.markdown("##### High-Frequency Wearable Telemetry Ingestion Layer")
st.write("Upload raw CSV/JSON sensor payloads, align native hardware schemas to standardized coordinate systems, and verify structural data integrity.")

# Comprehensive Health Informatics Deep Dive Panel
if show_explanation:
    with st.expander("🔬 Health Informatics Architecture: BioMAD + SKDH Core Framework", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧮 1. BioMAD Layer (The Signal Metric)")
            st.markdown(
                """
                **BioMAD** utilizes a modified **Mean Absolute Deviation (MAD)** calculation applied specifically to biotelemetry. 
                * **The Problem:** Raw triaxial accelerometer vectors ($A_x, A_y, A_z$) shift constantly based on how a patient positions or rotates their arm/wrist, meaning gravity heavily distorts the data.
                * **The Solution:** BioMAD isolates human movement from static gravitational force by calculating absolute deviations from a rolling mean stream. This provides a clean, rotation-invariant metric of physical effort.
                """
            )
            
        with col2:
            st.markdown("### 🚀 2. SKDH Layer (The Clinical Pipeline)")
            st.markdown(
                """
                **Scikit-Digital-Health (SKDH)** takes the raw metric streams processed by BioMAD and maps them over continuous longitudinal timeframes.
                * **Wear-Time Detection:** Automatically identifies and filters out windows where the patient took off the device.
                * **Digital Biomarkers:** Packages the signal sequences into standardized, regulatory-ready endpoints:
                  * 🏃‍♂️ **Gait Signature:** Stride variability, symmetry, and rhythmicity.
                  * 😴 **Sleep Architecture:** Rest-activity cycles, sleep efficiency, and circadian patterns.
                  * 📉 **Activity Biomarkers:** Stratifying movement into Sedentary, Light, or MVPA intensities.
                """
            )
            
        st.markdown("---")
        st.caption(
            "⚠️ **Data Lineage Summary:** Raw Sensor Hardware Stream ➡️ Column Mapping (This Dashboard) "
            "➡️ BioMAD Signal Filtering ➡️ SKDH Biomarker Extraction ➡️ Clinical Trial Endpoint Database."
        )

# ==========================================
# 3. FILE HANDLING & INGESTION STATUS
# ==========================================
st.write("---")
uploaded_file = st.file_uploader(
    "Upload raw high-frequency telemetry dataset", 
    type=["csv", "json"]
)

if uploaded_file is not None:
    st.success("🎉 Payload successfully cached in memory. Column schemas are ready for mapping validation.")
else:
    st.info(
        "💡 **Getting Started:** Drop a telemetry data file above. The active mapping configuration on the left "
        "will map incoming vectors into the unified BioMAD metric processing algorithm."
    )
