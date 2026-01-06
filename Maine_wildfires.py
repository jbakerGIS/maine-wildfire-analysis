"""
Maine Wildfire Analysis

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

CRS = "EPSG:2802"  # Maine State Plane (meters)

BASE_DIR = Path(r"C:/Users/viver/OneDrive/Desktop/Portfolio/Maine")

FIRE_DATA = BASE_DIR / "Fires.json"
STATE_DATA = BASE_DIR / "gz_2010_us_040_00_500k.json"
COUNTY_DATA = BASE_DIR / "Counties.geojson"

OUTPUT_HTML = BASE_DIR / "fires_explore.html"


# ------------------------------------------------------------------------------
# Data Loading Functions
# ------------------------------------------------------------------------------

def load_wildfires(path: Path, crs: str) -> gpd.GeoDataFrame:
    """
    Load wildfire point data and project to the target CRS.
    """
    return gpd.read_file(path).to_crs(crs)


def load_maine_boundary(path: Path, crs: str) -> gpd.GeoDataFrame:
    """
    Load U.S. state boundaries and extract Maine only.
    """
    states = gpd.read_file(path).to_crs(crs)
    return states.loc[states["NAME"] == "Maine"]


def load_counties(path: Path, crs: str) -> gpd.GeoDataFrame:
    """
    Load Maine county boundaries.
    """
    counties = gpd.read_file(path).to_crs(crs)
    return counties[["Name", "geometry"]]


# ------------------------------------------------------------------------------
# Analysis Functions
# ------------------------------------------------------------------------------

def calculate_fires_by_county(
    fires: gpd.GeoDataFrame,
    counties: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Spatially join wildfire points to counties and calculate
    fire counts per county.
    """
    joined = gpd.sjoin(
        fires,
        counties,
        predicate="within",
        how="inner"
    )

    fire_counts = (
        joined
        .groupby("Name")
        .size()
        .reset_index(name="Number of Fires")
    )

    county_fires = counties.merge(
        fire_counts,
        on="Name",
        how="left"
    )

    # Counties with no fires should display zero, not NaN
    county_fires["Number of Fires"] = (
        county_fires["Number of Fires"].fillna(0)
    )

    return county_fires


# ------------------------------------------------------------------------------
# Visualization Functions
# ------------------------------------------------------------------------------

def plot_wildfire_locations(
    maine: gpd.GeoDataFrame,
    fires: gpd.GeoDataFrame
) -> None:
    """
    Create a static map of wildfire locations in Maine.
    """
    fig, ax = plt.subplots(figsize=(9, 9))

    maine.plot(
        ax=ax,
        color="lightgray",
        edgecolor="black"
    )

    fires.plot(
        ax=ax,
        color="red",
        markersize=5
    )

    cx.add_basemap(ax, crs=fires.crs)

    ax.set_title("Wildfire Locations in Maine (2022)")
    ax.axis("off")

    plt.show()


def plot_fires_by_county(
    county_fires: gpd.GeoDataFrame
) -> None:
    """
    Create a choropleth map showing wildfire counts per county.
    """
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


def export_interactive_map(
    county_fires: gpd.GeoDataFrame,
    output_path: Path
) -> None:
    """
    Export an interactive web map of wildfires per county.
    """
    m = county_fires.explore(
        column="Number of Fires",
        cmap="Reds",
        legend=True
    )

    m.save(output_path)
    print(f"Interactive map saved to: {output_path}")


# ------------------------------------------------------------------------------
# Main Workflow
# ------------------------------------------------------------------------------

def main() -> None:
    """
    Execute the full GIS analysis workflow.
    """
    fires = load_wildfires(FIRE_DATA, CRS)
    maine = load_maine_boundary(STATE_DATA, CRS)
    counties = load_counties(COUNTY_DATA, CRS)

    plot_wildfire_locations(maine, fires)

    county_fires = calculate_fires_by_county(fires, counties)

    plot_fires_by_county(county_fires)
    export_interactive_map(county_fires, OUTPUT_HTML)


if __name__ == "__main__":
    main()
