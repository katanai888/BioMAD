import streamlit as st
import pandas as pd
import numpy as np

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
# 3. FILE HANDLING & INGESTION PROCESSING
# ==========================================
st.write("---")
uploaded_file = st.file_uploader(
    "Upload raw high-frequency telemetry dataset", 
    type=["csv", "json"]
)

if uploaded_file is not None:
    try:
        # Load data based on format
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_json(uploaded_file)
            
        # Verify columns exist
        required_cols = [timestamp_col, accel_x_col, accel_y_col, accel_z_col]
        missing_cols = [c for c in required_cols if c not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Structural Mapping Failed! Missing columns in payload: {missing_cols}")
            st.warning("Please adjust the active key mapping in the sidebar panel to match your source data headers.")
        else:
            st.success("🎉 Payload parsed successfully! Computing clinical metrics...")
            
            # Extract arrays based on user mapping
            x = df[accel_x_col].values
            y = df[accel_y_col].values
            z = df[accel_z_col].values
            
            # --- BioMAD Real-time Algorithm Execution ---
            # 1. Calculate vector magnitude
            vm = np.sqrt(x**2 + y**2 + z**2)
            # 2. Compute Mean Absolute Deviation (MAD) as a movement indicator
            biomad_score = np.abs(vm - np.mean(vm))
            df['BioMAD_Movement_Intensity'] = biomad_score
            
            # Display processing summary metrics
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Total Data Packets Ingested", f"{len(df):,}")
            m_col2.metric("Mean Movement Magnitude", f"{np.mean(vm):.3f} g")
            m_col3.metric("Computed BioMAD Intensity", f"{np.mean(biomad_score):.3f} g")
            
            # Plot data streams side by side
            st.subheader("📊 Processing Execution Telemetry")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown("**Mapped Input Waveforms (Gravity Contaminated)**")
                st.line_chart(df[[accel_x_col, accel_y_col, accel_z_col]].head(1000))
                
            with chart_col2:
                st.markdown("**Processed BioMAD Movement Output (Gravity Isolated for SKDH Pipeline)**")
                st.line_chart(df[['BioMAD_Movement_Intensity']].head(1000))
                
            # Data Frame Preview
            st.write("### Data Preview (First 5 Ingested Epochs)")
            st.dataframe(df[[timestamp_col, accel_x_col, accel_y_col, accel_z_col, 'BioMAD_Movement_Intensity']].head())
            
    except Exception as e:
        st.error(f"Error parsing file dataset structure: {e}")
else:
    st.info(
        "💡 **Getting Started:** Drop a telemetry data file above. The active mapping configuration on the left "
        "will map incoming vectors into the unified BioMAD metric processing algorithm."
    )
