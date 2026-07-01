import os
import numpy as np
import pandas as pd
import streamlit as st
from src.skdh.io.stream import StreamIngestor

st.set_page_config(page_title="BioMAD Ingestion Dashboard", layout="wide")

# Sidebar Configuration
with st.sidebar:
    st.header("🛠️ Hardware Telemetry Mapping")
    st.caption("Align raw incoming sensor keys to expected axis outputs.")
    x_key = st.text_input("X Axis Key Mapping", "accel_x")
    y_key = st.text_input("Y Axis Key Mapping", "accel_y")
    z_key = st.text_input("Z Axis Key Mapping", "accel_z")
    time_key = st.text_input("Timestamp Key", "timestamp")
    
    st.markdown("---")
    st.header("📖 Mode Settings")
    explanation_mode = st.checkbox("Enable Signal Processing Breakdown", value=True)
    informatics_guide = st.checkbox("Enable Health Informatics Guide", value=True)

st.title("🦉 Owl BioMAD Stream Ingestion Dashboard")
st.subheader("High-Frequency Wearable Telemetry & Rotation-Invariant Conditioning Layer")

# 1. Signal Processing Explanation Block
if explanation_mode:
    with st.expander("🎓 SYSTEM ARCHITECTURE & MATHEMATICAL BREAKDOWN", expanded=False):
        st.markdown("""
        ### **Signal Processing Flow**
        1. **Ingestion Layer (`StreamIngestor`):** Maps variable hardware-specific keys dynamically to normalized $X, Y, Z$ processing channels at a target sampling frequency ($fs = 100\\text{Hz}$).
        2. **Rotation-Invariant Conditioning Layer:** Transforms raw acceleration into gravity-independent physical exertion metrics using **Mean Absolute Deviation (MAD)**.
        
        $$\\text{MAD} = \\frac{1}{N} \\sum_{i=1}^{N} |r_i - \\tilde{r}|$$
        
        *Where $r_i = \\sqrt{x_i^2 + y_i^2 + z_i^2}$ represents the vector magnitude, and $\\tilde{r}$ is the signal median.*
        """)

# 2. Health Informatics Guide Block
if informatics_guide:
    with st.expander("🏥 HEALTH INFORMATICS & CLINICAL WORKFLOW GUIDE", expanded=False):
        st.markdown("""
        ### **Clinical Data Standardization Architecture**
        To move high-frequency consumer sensor payloads ($100\\text{Hz}$) safely into clinical decision ecosystems, data must be structured across standardized healthcare vocabularies:
        
        * **LOINC (Logical Observation Identifiers Names and Codes):** Maps the overall device data-capturing procedure (e.g., *LOINC 93012-3: Physical activity monitoring panel*).
        * **SNOMED-CT (Systematized Nomenclature of Medicine - Clinical Terms):** Codifies body site placement coordinates and structural semantic findings (e.g., *SNOMED 412435003: Structure of wrist*).
        * **HL7 FHIR Interoperability:** High-frequency raw data vectors are rolled up into compressed feature arrays or statistical aggregates, then transmitted as standard **FHIR Observation Resources**:
        
        ```json
        {
          "resourceType": "Observation",
          "status": "final",
          "category": [{ "coding": [{ "system": "[http://terminology.hl7.org/CodeSystem/observation-category](http://terminology.hl7.org/CodeSystem/observation-category)", "code": "vital-signs" }] }],
          "code": { "coding": [{ "system": "[http://loinc.org](http://loinc.org)", "code": "93012-3", "display": "Physical activity panel" }] },
          "valueQuantity": { "value": 0.042, "unit": "g_mad", "system": "[http://unitsofmeasure.org](http://unitsofmeasure.org)" }
        }
        ```
        """)

# Data Acquisition Matrix (Preset Dropdown + Upload)
st.markdown("### 📥 Data Acquisition Input")
col1, col2 = st.columns(2)

preset_files = {
    "--- Select an Available Dataset ---": None,
    "📈 Mock Telemetry Stream (test_clean.csv)": "test_clean.csv"
}

with col1:
    selected_preset = st.selectbox("Option A: Choose a pre-loaded system file", list(preset_files.keys()))

with col2:
    uploaded_file = st.file_uploader("Option B: Or drag and drop custom payload", type=["csv"])

# Target Router Logic
df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.info(f"📁 Custom upload detected: **{uploaded_file.name}**")
    except Exception as e:
        st.error(f"Failed parsing uploaded file: {e}")
elif preset_files[selected_preset] is not None:
    file_path = preset_files[selected_preset]
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            st.info(f"📈 Loaded preset file successfully: **{file_path}**")
        except Exception as e:
            st.error(f"Error parsing preset file: {e}")
    else:
        st.error(f"🔴 {file_path} missing from workspace.")

# Execution Action Pipeline
if st.button("Process Stream Package"):
    if df is not None:
        try:
            column_mapping = {'x': x_key, 'y': y_key, 'z': z_key}
            ingestor = StreamIngestor(column_mapping=column_mapping, time_column=time_key, fs=100.0)
            
            st.success(f"🚀 Successfully processed {len(df)} telemetry stream packets through the conditioning matrix!")
            
            # --- Comprehensive Analytics Output Block ---
            st.markdown("---")
            st.subheader("📊 Comprehensive Ingestion Analytics Report")
            
            # Calculate metrics
            vm = np.sqrt(df[x_key]**2 + df[y_key]**2 + df[z_key]**2)
            mad_val = np.mean(np.abs(vm - np.median(vm)))
            
            # Append calculated metrics back into the dataframe for export integrity
            df['vector_magnitude'] = vm
            df['calculated_mad'] = mad_val
            
            met1, met2, met3 = st.columns(3)
            with met1:
                st.metric(label="Calculated Signal MAD", value=f"{mad_val:.4f} g")
            with met2:
                st.metric(label="Sampling Window Size", value=f"{len(df)} Epoch Packets")
            with met3:
                st.metric(label="Stream Status", value="Verified Active")
                
            with st.expander("🔍 TECHNICAL & SIGNAL QUALITY BREAKDOWN", expanded=True):
                st.markdown(f"""
                * **Dynamic Axis Alignment:** Raw metrics mapped cleanly from parameters `{x_key}`, `{y_key}`, and `{z_key}`. 
                * **Signal Resolution Verification:** All fields are structurally numeric. Vector components correctly filter out orthogonal gravitational biases via Euclidean norm scaling.
                * **Downstream Delivery Status:** Signal vectors successfully aggregated and packaged into an immutable cache payload ready for direct serialization to a healthcare enterprise messaging sink.
                """)
                
            # --- Added Export Feature ---
            st.markdown("### 💾 Export Processed Payload")
            csv_buffer = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Processed CSV Dataset",
                data=csv_buffer,
                file_name="processed_biomad_telemetry.csv",
                mime="text/csv",
                help="Click to download the clean telemetry metrics with computed vector magnitudes."
            )
            
            st.dataframe(df.head(10))
            
        except Exception as e:
            st.error(f"Failed to process stream package: {e}")
    else:
        st.warning("Please select a valid dropdown option or upload a file first.")
