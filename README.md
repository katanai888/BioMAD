

# 📦 BioMAD

**biomad** is a simple drag-and-drop tool that takes raw movement data from wearable sensors (like smartwatches or research trackers) and turns it into clean, useful health metrics.

It acts as an easy-to-use bridge for [Scikit Digital Health (SKDH)](https://scikit-digital-health.readthedocs.io/en/latest/). While SKDH usually expects specific file formats from certain brands, **biomad** lets you feed in raw data from *any* device using a simple web dashboard.

---

## ❓ Why It Matters

When tracking movement in clinical trials, you run into two big problems:

1. **Wrong Formats:** Legacy software expects fixed files, but modern apps capture data in raw, continuous streams (like JSON or CSV dumps).
2. **Naming Confusion:** Different watches use different names for the same thing (one calls it `accel_x`, another calls it `acceleration_X`).

**biomad** fixes this by giving you a simple setup screen where you can instantly match any device's data labels to a unified system.

---

## 🧮 How Data Flows

```text
Raw Watch Data ──> Label Mapping (Dashboard) ──> BioMAD Clean Filter ──> SKDH Health Metrics

```

### 1. The BioMAD Filter (Cleaning Gravity)

If a patient rotates their wrist, the sensor data shifts drastically just from the pull of gravity. The **BioMAD** layer calculates a rolling **Mean Absolute Deviation (MAD)**. It filters out constant gravitational pulls so you only measure the patient's actual physical effort.

### 2. The SKDH Layer (The Health Insights)

Once the data is cleaned, it passes into the core health pipeline to calculate real-world endpoints:

* 🏃‍♂️ **Gait:** Measuring stride cadence, rhythm, and symmetry.
* 😴 **Sleep:** Tracking rest-activity cycles and sleep efficiency.
* 📉 **Activity Levels:** Grouping daily movement into Sedentary, Light, or Heavy exercise.

---

## 🚀 Run the Dashboard

To open the user-friendly drag-and-drop web app interface locally or in your Codespace, run this command in your terminal:

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

## 📜 Citation & License

If you use this pipeline or the underlying `SKDH` framework for academic research, please cite:

```text
[1] L. Adamowicz, Y. Christakis, M. D. Czech, and T. Adamusiak, “SciKit Digital Health: Python Package for Streamlined Wearable Inertial Sensor Data Processing,” JMIR mHealth and uHealth, vol. 10, no. 4, p. e36762, Apr. 2022, doi: 10.2196/36762.

```

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
