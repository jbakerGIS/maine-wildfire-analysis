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

## 🗂 Project Structure
'''
maine-wildfire-analysis/
├── src/
│   ├── main.py                    # Main entry point for analysis workflow
│   ├── analysis.py                # Spatial analysis & aggregation functions
│   └── visualization.py           # Static & interactive mapping functions
│
├── data/
│   ├── raw/                       # Original datasets (not tracked by Git)
│   ├── processed/                 # Cleaned / derived datasets
│   └── README.md                  # Data sources & licensing notes
│
├── docs/
│   ├── index.html                 # GitHub Pages landing page
│   ├── fires_by_county_2022.html  # Interactive web map (hosted via Pages)
│   ├── images/
│   │   ├── wildfire_locations_2022.png
│   │   └── wildfire_counts_by_county_2022.png
│   └── workflow.md                # Plain-language analysis explanation
│
├── notebooks/
│   └── exploration.ipynb          # Exploratory analysis & prototyping
│
├── outputs/
│   └── figures/                   # Generated static map outputs
│
├── tests/
│   └── test_spatial_joins.py      # (Optional) spatial logic validation
│
├── .gitignore
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview & results
└── LICENSE
'''
🌐 **View the interactive map:**  
Open [fires_by_county_2022.html](https://jbakergis.github.io/maine-wildfire-analysis/fires_by_county_2022.html)

**Map features include:**
- Pan and zoom
- County-level wildfire counts
- Hover-based inspection
