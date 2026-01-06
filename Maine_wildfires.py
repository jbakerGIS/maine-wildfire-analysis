"""
Maine Wildfire Analysis (2022)

Author: Justin Baker
Created: September 2023

Description:
    This script visualizes wildfire locations in Maine and summarizes
    wildfire counts by county using GeoPandas. It produces both static
    maps and an interactive HTML map.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

# Coordinate Reference System (Maine State Plane, meters)
CRS = "EPSG:2802"

# Project directory (update if needed)
BASE_DIR = Path(r"C:/Users/viver/OneDrive/Desktop/Portfolio/Maine")

# Input data paths
FIRE_DATA = BASE_DIR / "Fires.json"
STATE_DATA = BASE_DIR / "gz_2010_us_040_00_500k.json"
COUNTY_DATA = BASE_DIR / "Counties.geojson"

# Output paths
OUTPUT_HTML = BASE_DIR / "fires_explore.html"


# ------------------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------------------

# Read wildfire point data
fires = gpd.read_file(FIRE_DATA).to_crs(CRS)

# Read U.S. states and extract Maine boundary
states = gpd.read_file(STATE_DATA).to_crs(CRS)
maine = states.loc[states["NAME"] == "Maine"]


# ------------------------------------------------------------------------------
# Static Map: Wildfire Locations
# ------------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 9))

# Plot Maine boundary
maine.plot(ax=ax, color="lightgray", edgecolor="black")

# Plot wildfire points
fires.plot(ax=ax, color="red", markersize=5)

# Add basemap
cx.add_basemap(ax, crs=fires.crs)

ax.set_title("Wildfire Locations in Maine (2022)")
ax.axis("off")

plt.show()


# ------------------------------------------------------------------------------
# Wildfires by County
# ------------------------------------------------------------------------------

# Read county boundaries
counties = gpd.read_file(COUNTY_DATA).to_crs(CRS)

# Keep only relevant columns
counties = counties[["Name", "geometry"]]

# Spatially join fires to counties
fires_by_county = gpd.sjoin(
    fires,
    counties,
    predicate="within",
    how="inner"
)

# Count number of fires per county
fire_counts = (
    fires_by_county
    .groupby("Name")
    .size()
    .reset_index(name="Number of Fires")
)

# Merge counts back to county geometries
county_fires = counties.merge(fire_counts, on="Name", how="left")

# Replace NaN values with zero for counties with no fires
county_fires["Number of Fires"] = county_fires["Number of Fires"].fillna(0)


# ------------------------------------------------------------------------------
# Static Map: Fires per County
# ------------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 9))

county_fires.plot(
    column="Number of Fires",
    cmap="Reds",
    legend=True,
    ax=ax,
    edgecolor="black"
)

ax.set_title("Maine Wildfires per County (2022)")
ax.axis("off")

plt.show()


# ------------------------------------------------------------------------------
# Interactive Map Export
# ------------------------------------------------------------------------------

# Create interactive map and save to HTML
interactive_map = county_fires.explore(
    column="Number of Fires",
    cmap="Reds",
    legend=True
)

interactive_map.save(OUTPUT_HTML)

print(f"Interactive map saved to: {OUTPUT_HTML}")

