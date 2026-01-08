# Maine Wildfire Analysis

An analysis of wildfire activity in Maine using open data from national and state sources.  
This project demonstrates how to pull, process, and visualize wildfire perimeter and county boundary data using **GeoPandas**, and generate both static figures and interactive outputs.

## 📌 Overview

Wildfires are an important environmental and land management issue in Maine, a heavily forested state with hundreds of fire events annually. This repository provides scripts and outputs to explore wildfire patterns, map fire perimeters, and generate geospatial visualizations.

Data sources used:
- **National Interagency Fire Center (NIFC)** – Wildfire perimeter data  
  https://data-nifc.opendata.arcgis.com/
- **OpenDataSoft** – County boundary data  
  https://public.opendatasoft.com/

## 🧭 Workflow Summary

This project follows a reproducible GIS analysis workflow implemented in Python using GeoPandas:

1. **Data ingestion**  
   Public wildfire, state boundary, and county boundary datasets are loaded from the `data/raw/` directory.

2. **CRS standardization**  
   All datasets are reprojected to a common coordinate reference system (EPSG:2802 – Maine State Plane) to ensure spatial accuracy.

3. **Boundary processing**  
   - The national state boundary dataset is filtered to extract Maine  
   - County boundaries are cleaned and subset to essential attributes  
   - Processed boundary layers are exported to `data/processed/`

4. **Spatial analysis**  
   Wildfire point locations are spatially joined to county polygons and aggregated to calculate wildfire counts per county.

5. **Visualization and outputs**  
   - Static maps are generated for wildfire locations and county-level summaries  
   - An interactive HTML web map is exported to the `docs/` directory and published via GitHub Pages

All outputs are generated programmatically and can be reproduced by rerunning the analysis script.

## 🗂 Project Structure
```text
maine-wildfire-analysis/
├── src/
│   ├── main.py                    # Main entry point for analysis workflow
│   ├── analysis.py                # Spatial analysis & aggregation functions
│   └── visualization.py           # Static & interactive mapping functions
│
├── data/
│   ├── raw/                       # Original datasets
│   ├── processed/                 # Cleaned / derived datasets
│   └── README.md                  # Data sources & licensing notes
│
├── docs/
│   ├── index.html                 # GitHub Pages landing page
│   ├── fires_by_county_2022.html  # Interactive web map (hosted via Pages)
│   └── workflow.md                # Plain-language analysis explanation
│
├── notebooks/
│   └── analysis_notebook.ipynb          # Exploratory analysis & prototyping
│
├── outputs/
│   └── figures/                   # Generated static map outputs
│
├── .gitignore
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview & results
└── LICENSE
```
## 🖼️ Output Maps


🌐 **View the interactive map:**  
Open [fires_by_county_2022.html](https://jbakergis.github.io/maine-wildfire-analysis/fires_by_county_2022.html)

**Map features include:**
- Pan and zoom
- County-level wildfire counts
- Hover-based inspection

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Set up a Python environment

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add raw data
```bash
data/raw
```

### 5. Run the analysis
```bash
python src/main.py
```

### 6. View outputs
- Static maps will be displayed during execution
- Processed datasets will be written to data/processed/
- The interactive web map will be exported to:
```bash
docs/fires_by_county_2022.htmml
```
