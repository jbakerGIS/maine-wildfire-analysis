"""
--------------------------------------------------------------------------------
Maine Wildfire Analysis
Author: Justin Baker
Date: September 2023
--------------------------------------------------------------------------------

Description:
    This script visualizes wildfire locations in Maine and summarizes
    wildfire counts by county using GeoPandas. It produces both static
    maps and an interactive HTML map.

--------------------------------------------------------------------------------
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx


# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

CRS = "EPSG:2802"  # Maine State Plane (meters)

FIRE_DATA = Path("./data/raw/Fires.json")
STATE_DATA = Path("./data/raw/gz_2010_us_040_00_500k.json")
COUNTY_DATA = Path("./data/raw/Counties.geojson")

PROCESSED_MAINE_BOUNDARY = Path("../data/processed/maine_boundary.gpkg")
PROCESSED_COUNTIES = Path("../data/processed/maine_counties.gpkg")
OUTPUT_HTML = Path("./docs/fires_by_county_2022.html")

# ------------------------------------------------------------------------------
# Export Function
# ------------------------------------------------------------------------------

def export_geodataframe(
    gdf: gpd.GeoDataFrame,
    output_path: Path,
    layer_name: str | None = None
) -> None:
    '''
    Export a GeoDataFrame to disk, creating parent directories if needed.
    '''
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix == ".gpkg":
        gdf.to_file(output_path, layer=layer_name, driver="GPKG")
    else:
        gdf.to_file(output_path)

    print(f"Exported: {output_path}")


# ------------------------------------------------------------------------------
# Data Loading Functions
# ------------------------------------------------------------------------------

def load_wildfires(path: Path, crs: str) -> gpd.GeoDataFrame:
    '''Load wildfire point data and project to the target CRS.'''
    
    return gpd.read_file(path).to_crs(crs)


def load_maine_boundary(
        path: Path,
        crs: str,
        export: bool = True
) -> gpd.GeoDataFrame:
    '''
    Load U.S. state boundaries and extract Maine, and optionally export
    the processed boundary.
    '''

    states = gpd.read_file(path).to_crs(crs)
    maine = states.loc[states["NAME"] == "Maine"]

    if export:
        export_geodataframe(
            maine,
            PROCESSED_MAINE_BOUNDARY,
            layer_name="maine_boundary"
        )
    return states.loc[states["NAME"] == "Maine"]


def load_counties(
    path: Path,
    crs: str,
    export: bool = True
) -> gpd.GeoDataFrame:
    '''
    Load Maine county boundaries and optionally export
    the processed dataset.
    '''

    counties = gpd.read_file(path).to_crs(crs)
    counties = counties[["name", "geometry"]]

    if export:
        export_geodataframe(
            counties,
            PROCESSED_COUNTIES,
            layer_name="maine_counties"
        )

    return counties


# ------------------------------------------------------------------------------
# Analysis Functions
# ------------------------------------------------------------------------------

def calculate_fires_by_county(
    fires: gpd.GeoDataFrame,
    counties: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    '''
    Spatially join wildfire points to counties and calculate
    fire counts per county.
    '''
    
    joined = gpd.sjoin(
        fires,
        counties,
        predicate="within",
        how="inner"
    )

    fire_counts = (
        joined
        .groupby("name")
        .size()
        .reset_index(name="Number of Fires")
    )

    county_fires = counties.merge(
        fire_counts,
        on="name",
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
    '''Create a static map of wildfire locations in Maine.'''
    
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
    '''Create a choropleth map showing wildfire counts per county.'''

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
    '''Export an interactive web map of wildfires per county.'''
    

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
    '''Execute the full GIS analysis workflow.'''
    fires = load_wildfires(FIRE_DATA, CRS)
    maine = load_maine_boundary(STATE_DATA, CRS)
    counties = load_counties(COUNTY_DATA, CRS)

    plot_wildfire_locations(maine, fires)

    county_fires = calculate_fires_by_county(fires, counties)

    plot_fires_by_county(county_fires)
    export_interactive_map(county_fires, OUTPUT_HTML)


if __name__ == "__main__":
    main()