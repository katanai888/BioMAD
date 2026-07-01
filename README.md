
# 🦉 BioMAD

An open-source stream ingestion gateway and conditioning pipeline that decodes raw IMU sensor data from any wearable device into clean, standardized digital health metrics.

---

## ❓ Why It Matters

In digital health and clinical trials, wearable devices capture continuous, real-time insights into a patient’s daily life. However, data engineers and clinical researchers frequently hit two frustrating roadblocks:

1. **Data Fragmentation & Label Confusion:** Data ingestion is stalled by rigid file formats and naming inconsistencies across consumer or medical-grade device brands. One device outputs a file with `accel_x`, while another outputs a stream labeled `acceleration_X`.
2. **Environmental Noise:** Raw Inertial Measurement Unit (IMU) data is incredibly noisy. If a patient simply rotates their wrist while sitting, the sudden shift in gravitational pull can heavily skew movement calculations, leading to inaccurate clinical endpoints.

**BioMAD** bridges this gap. It acts as a flexible, vendor-agnostic gateway where researchers can feed raw data streams from any wearable device, dynamically map them, and isolate genuine human physical effort.

---

## 🧮 How Data Flows

```
Raw Watch Data ──> Label Mapping (Dashboard) ──> BioMAD Clean Filter ──> SKDH Health Metrics

```

### 1. Zero-Code Label Mapping (The Dashboard)

No more custom, hardcoded parsing scripts. The pipeline features a user-friendly, drag-and-drop web dashboard built with Streamlit, allowing clinical teams to instantly map any incoming device labels to a unified system on the fly.

### 2. Invariant Telemetry Conditioning (The BioMAD Filter)

To remove constant gravitational pulls, the conditioning pipeline applies a rolling **Mean Absolute Deviation (MAD)** calculation. This filters out the gravity artifacts so downstream models measure the patient's *actual physical effort* and genuine kinetic movement.

### 3. Clinical Health Insights

Once the data layer is cleaned and standardized, it passes seamlessly into core digital health frameworks to calculate real-world clinical endpoints:

* 🏃‍♂️ **Gait Analysis:** Measuring stride cadence, rhythm, and symmetry.
* 😴 **Sleep Quality:** Tracking rest-activity cycles and sleep efficiency.
* 📉 **Activity Biomarkers:** Grouping daily movement into Sedentary, Light, or Heavy exercise.

---

## 🚀 Run the Dashboard

To launch the interactive drag-and-drop web app interface locally or in your GitHub Codespace, run this command in your terminal:

```bash
export PYTHONPATH=src
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

```

---

## 🛠️ Installation

First, install the core digital health package:

```bash
pip install scikit-digital-health

```

*(Windows users: You might need to install the Microsoft Visual C++ Redistributable >14.0).*

Next, install the dashboard tools:

```bash
pip install streamlit pandas

```

---

## 📜 Citations & References

If you utilize this pipeline in academic literature or clinical trial reporting, please cite the software and its underlying core library framework as follows:

```text
[1] K. Usop, “BioMAD: A Stream-Based Digital Biomarker Ingestion and Invariant Telemetry Conditioning Gateway,” July 2026. Available: https://github.com/katanai888/biomad

[2] L. Adamowicz, Y. Christakis, M. D. Czech, and T. Adamusiak, “SciKit Digital Health: Python Package for Streamlined Wearable Inertial Sensor Data Processing,” JMIR mHealth and uHealth, vol. 10, no. 4, p. e36762, Apr. 2022, doi: 10.2196/36762.

```

This project is open-source and available under the [MIT License](https://github.com/katanai888/BioMAD).
