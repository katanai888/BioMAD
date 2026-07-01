import streamlit as st
import pandas as pd
import json
import importlib.util

# Set up page configuration
st.set_page_config(page_title="BioMAD Ingestion Dashboard", page_icon="🦉", layout="wide")

st.title("🦉 BioMAD Stream Ingestion Dashboard")
st.subheader("High-Frequency Wearable Telemetry & Rotation-Invariant Conditioning Layer")
st.markdown(
    "Upload raw CSV/JSON sensor payloads, align native hardware schemas, "
    "and isolate physical exertion using the **BioMAD (Mean Absolute Deviation)** filtering matrix."
)

# Dynamically load StreamIngestor to bypass missing compiled math extensions
spec = importlib.util.spec_from_file_location('skdh.io.stream', 'src/skdh/io/stream.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
StreamIngestor = module.StreamIngestor

# Sidebar configuration for column mapping
st.sidebar.header("🛠️ Hardware Telemetry Mapping")
st.sidebar.markdown("Align your raw incoming sensor keys to the expected axis outputs.")

mapping_x = st.sidebar.text_input("X Axis Key Mapping", "accel_x")
mapping_y = st.sidebar.text_input("Y Axis Key Mapping", "accel_y")
mapping_z = st.sidebar.text_input("Z Axis Key Mapping", "accel_z")
time_key = st.sidebar.text_input("Timestamp Key", "timestamp")

# File Upload Mechanism
uploaded_file = st.file_uploader("Drag and drop your raw sensor payload here (CSV or JSON)", type=["csv", "json"])

if uploaded_file is not None:
    try:
        # Parse based on file type
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.DataFrame(json.load(uploaded_file))
            
        st.success(f"Successfully loaded {len(df_raw)} raw data packets!")
        
        # Build the column layout dictionary dynamically from UI inputs
        column_mapping = {
            mapping_x: 'x',
            mapping_y: 'y',
            mapping_z: 'z'
        }
        
        # Instantiate and run the ingestor stream layer
        ingestor = StreamIngestor(column_mapping=column_mapping, time_col=time_key)
        processed_data = ingestor.ingest(df_raw)
        
        # Visualize the metrics
        st.header("📈 Normalized Acceleration Output")
        
        if 'accel' in processed_data and processed_data['accel'].shape[0] > 0:
            # Reconstruction for line chart compatibility
            accel_matrix = processed_data['accel']
            chart_df = pd.DataFrame(accel_matrix, columns=['X-Axis', 'Y-Axis', 'Z-Axis'])
            
            if 'time' in processed_data:
                chart_df['Time'] = pd.to_datetime(processed_data['time'], unit='s', errors='coerce')
                chart_df = chart_df.set_index('Time')
                
            st.line_chart(chart_df)
            
            # Metadata analysis dump
            with st.expander("🔍 View Ingested Pipeline Payload Object"):
                st.json({
                    "sample_count": len(chart_df),
                    "keys_extracted": list(processed_data.keys()),
                    "shape": str(accel_matrix.shape)
                })
        else:
            st.warning("Data successfully read, but could not map into valid structures. Review your sidebar axis labels.")
            
    except Exception as e:
        st.error(f"Failed to process stream package: {str(e)}")
else:
    st.info("💡 Waiting for a telemetry stream input file to begin conditioning layer parsing.")

# --- Explanation Mode ---
st.markdown("---")
show_explanation = st.checkbox("📖 Enable Explanation Mode", value=True)

if show_explanation:
    st.header("🧠 Core Mechanics: BioMAD & Conditioning Layer")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Stream Alignment & Conditioning")
        st.markdown(
            "Raw wearable devices output highly variable JSON/CSV payload keys depending on the hardware vendor "
            "(e.g., `accelX`, `A_X`, `mag_x`). The **Conditioning Layer** acts as an adaptive interface map, "
            "standardizing these arbitrary shapes into an immutable, structured NumPy array compatible with downstream ML pipelines."
        )
        
    with col2:
        st.subheader("2. Rotation-Invariant Signal Isolation")
        st.markdown(
            "Instead of relying on raw coordinate orientations—which flip constantly as a user moves their wrist or torso—"
            "the mathematical core isolates physical exertion using a variance metric. By tracking the Mean Absolute Deviation "
            "around signal medians, gravity is factored out without needing static orientation matrices or rigid device calibration."
        )

# --- Health Informatics Guide & Use Cases ---
st.markdown("---")
show_informatics_guide = st.checkbox("🩺 Open Health Informatics & Use Cases Guide", value=True)

if show_informatics_guide:
    st.header("📋 Health Informatics Deployment Framework")
    st.markdown(
        "Health informaticists bridge the gap between noisy consumer-grade wearable endpoints "
        "and structured, clinically actionable medical data storage (e.g., FHIR resources). "
        "Here is how this conditioning layer stabilizes digital health pipelines:"
    )
    
    # Use Case Tabs
    tab1, tab2, tab3 = st.tabs([
        "🔬 Clinical Research Validation", 
        "🔄 Cross-Vendor Interoperability", 
        "📈 Remote Patient Monitoring (RPM)"
    ])
    
    with tab1:
        st.subheader("Standardizing Physical Biomarkers")
        st.markdown(
            "**Scenario:** A multi-site clinical trial utilizes different device profiles across participant cohorts.\n\n"
            "* **The Challenge:** Raw acceleration magnitudes vary wildly depending on whether an individual wears an Apple Watch, "
            "Fitbit, or a medical-grade ActiGraph.\n"
            "* **The Solution:** By extracting the *Mean Absolute Deviation (MAD)* stream globally, researchers obtain an "
            "orientation-independent index of physical exertion that can be directly mapped to metabolic equivalents (METs) "
            "without needing vendor-specific proprietary filters."
        )
        
    with tab2:
        st.subheader("Data Harmonization for EHR Ingestion")
        st.markdown(
            "**Scenario:** Ingesting high-frequency telemetry into a centralized health database.\n\n"
            "* **The Challenge:** Sensor payloads use inconsistent naming schemas (`acc_x`, `accelerometerX`, `ax`).\n"
            "* **The Solution:** The *Hardware Telemetry Mapping* interface creates a predictable middleware schema. "
            "It maps arbitrary streams on-the-fly into standardized structural metrics fit for transactional database indexing."
        )
        
    with tab3:
        st.subheader("Isolating Artifacts in Long-Term Monitoring")
        st.markdown(
            "**Scenario:** Elderly patients monitored at home for gait tracking and frailty indicators.\n\n"
            "* **The Challenge:** Gravity components skew data if the sensor moves or flips on the patient's arm.\n"
            "* **The Solution:** Utilizing rotation-invariant algorithms strips out static gravity vectors dynamically, "
            "meaning accidental device rotations are treated as artifacts rather than false physical activity spikes."
        )
        
    # Citation & Contact Information Block
    st.info(
        "💡 **Informatics Project Citation & Inquiry**\n\n"
        "This architectural pattern and stream ingestion conditioning layer were conceptualized and developed by katusop.\n\n"
        "For system integration inquiries, custom electronic health record (EHR) pipelines, or architectural consultations, "
        "reach out via the official website: [katusop.co](https://katusop.co)"
    )
