# 🧭 GIS Analysis Workflow

This document describes the end-to-end workflow used in the Maine Wildfire Analysis project, from raw data ingestion to final map outputs. The goal of this workflow is to demonstrate a reproducible, well-structured GIS analysis pipeline using Python and GeoPandas.

## 1️⃣ Data Acquisition

This project uses publicly available geospatial datasets:

### Wildfire Occurrence Data
Source: National Interagency Fire Center (NIFC) ArcGIS Open Data
Format: GeoJSON
Geometry: Point features representing wildfire locations

### State Boundary Data
Source: U.S. Census Bureau (Cartographic Boundary Files)
Geometry: U.S. state polygons

### County Boundary Data
Source: OpenDataSoft
Geometry: County-level administrative boundaries for Maine

Raw datasets are downloaded manually and stored in:

    data/raw/


Raw data files are preserved in their original form and are not modified directly.

## 2️⃣ Coordinate Reference System Standardization

All spatial datasets are reprojected to a common coordinate reference system to ensure accurate spatial analysis:

CRS: EPSG:2802

Description: Maine State Plane (meters)

Reprojection occurs immediately after loading each dataset to maintain consistency throughout the workflow.

## 3️⃣ Boundary Extraction and Processing

### State Boundary Processing

The national state boundary dataset is filtered to extract Maine

The resulting Maine-only boundary is exported as a processed dataset

#### Output:

    data/processed/maine_boundary.gpkg

### County Boundary Processing

County boundaries are loaded and subset to essential attributes

The cleaned dataset is exported for reuse in analysis and mapping

#### Output:

    data/processed/maine_counties.gpkg


These processed boundaries serve as standardized inputs for all subsequent analysis steps.

## 4️⃣ Spatial Analysis

### Fire-to-County Spatial Join

Wildfire point locations are spatially joined to county polygons

Each wildfire is assigned to the county in which it occurred

### Aggregation

Wildfires are grouped by county

Total fire counts are calculated per county

Counties with no recorded fires are assigned a value of zero

#### Result:

A county-level dataset containing wildfire counts for 2022

## 5️⃣ Static Map Production

Two static maps are generated using Matplotlib and Contextily:

### Wildfire Locations Map

Displays individual wildfire points over the Maine state boundary

Includes a basemap for geographic context

#### Wildfires by County Map

Choropleth map showing the number of wildfires per county

Uses a sequential color ramp to emphasize variation in counts

These maps are intended for exploratory analysis and visual validation.

## 6️⃣ Interactive Web Map Export

An interactive choropleth map is created using GeoPandas’ .explore() method (Folium-based):

Displays wildfire counts by county

Includes hover interactivity and legend controls

Exported as a standalone HTML file

#### Output:

    docs/fires_by_county_2022.html


This file is hosted using GitHub Pages, allowing the interactive map to be viewed directly in a web browser without additional dependencies.

## 7️⃣ Outputs and Reproducibility

### Generated Outputs

Processed boundary datasets (data/processed/)

Static map figures (generated at runtime)

Interactive HTML web map (docs/)

### Reproducibility

To reproduce the analysis:

Download the raw datasets listed above

Place them in the data/raw/ directory

Run the main analysis script:

    python src/main.py


All outputs can be regenerated at any time by rerunning the script.

## 8️⃣ Design Considerations

This workflow emphasizes:

Clear separation of raw vs processed data

CRS consistency across datasets

Modular, function-based Python code

Path-safe file handling

Outputs suitable for both analysis and web presentation

These design choices reflect common best practices in professional GIS and geospatial data workflows.