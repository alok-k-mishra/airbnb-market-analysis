## Overview

This project presents an interactive analysis of **12,075 Airbnb listings and calendar availability records across the United States**. The analysis focuses on understanding how Airbnb listings differ across geographic locations, pricing ranges, property and room types, host characteristics, availability, and customer review activity.

The project combines **Python for data preparation and geographic processing** with **Tableau for interactive data visualization and dashboard development**. The final dashboard provides multiple analytical views that allow users to explore the Airbnb market at different levels of detail, from overall listing and pricing patterns to individual ZIP-code-level comparisons.

**Interactive Dashboard:** [View the Tableau Dashboard](https://public.tableau.com/views/AnalysisofAirbnbacrossTheUnitedStates/Dashboard1)

## Problem

Airbnb datasets contain a large amount of information about listings, prices, availability, property types, room types, hosts, locations, and customer reviews. While this information can provide valuable insights into the short-term rental market, analyzing the raw data directly can make it difficult to identify meaningful patterns and compare different markets.

The objective of this project was to transform the available Airbnb data into an interactive analytical dashboard that provides a clearer view of **pricing behavior, geographic distribution, listing characteristics, host information, availability, and customer review activity**.

A particular focus was placed on geographic analysis, allowing listings to be grouped by approximate ZIP codes. This makes it possible to compare Airbnb activity across different U.S. markets and examine how listing characteristics and pricing vary between locations.

## Approach

The project followed a data preparation, geographic processing, and visualization workflow.

* **Data Preparation:** Cleaned and prepared the Airbnb listing and calendar availability data so that the relevant fields could be analyzed consistently.
* **Geographic Processing:** Used Python to work with the latitude and longitude information associated with listings and map the coordinates to approximate ZIP codes.
* **Exploratory Analysis:** Examined variables related to listing prices, property types, room types, availability, hosts, and customer reviews to identify useful dimensions for comparison.
* **Dashboard Development:** Imported the prepared data into Tableau and developed multiple interactive views for exploring different aspects of the Airbnb market.
* **Calculated Fields:** Created Tableau calculated fields to derive metrics required for pricing, geographic, and listing-level analysis.
* **Interactive Exploration:** Structured the dashboard so users can explore the data across different locations and listing categories rather than relying on a single static visualization.

This workflow allowed the project to combine **data preparation in Python** with **interactive analytical storytelling in Tableau**.

## Tools & Skills

* **Python** — Used for data preparation and geographic processing, including working with latitude and longitude coordinates and mapping listings to approximate ZIP codes for location-based analysis.
* **Tableau** — Used to build the interactive dashboard and create visualizations for analyzing Airbnb pricing, listing distribution, property types, room types, host characteristics, availability, and review metrics.
* **Tableau Calculated Fields** — Used to create derived metrics and analytical calculations needed to compare listings and support the dashboard's pricing and geographic analysis.
* **Geospatial Analysis** — Used latitude/longitude coordinates and ZIP-code-level geographic information to examine how Airbnb listings are distributed across different U.S. markets.
* **Data Cleaning & Preparation** — Prepared listing and calendar availability data for consistent analysis and visualization, ensuring the information could be effectively used within Tableau.
* **Exploratory Data Analysis** — Examined different dimensions of the dataset to identify useful patterns and relationships that could be represented through dashboard visualizations.
* **Interactive Dashboard Design** — Organized multiple visualizations into a unified Tableau dashboard so users can move from high-level market patterns to more granular location and listing-level analysis.

## Data Files

The repository contains the raw Airbnb datasets used to build the Tableau dashboard:

* **`listings.csv`** — ~10,400 Airbnb listings with descriptive attributes (price, property/room type, host information, review scores, availability, and latitude/longitude coordinates). This is the primary file used for geographic and pricing analysis.
* **`calendar.csv`** — Daily price and availability records per listing, used for availability analysis.
* **`reviews.csv`** — Individual customer review records per listing, used for review-activity analysis.
* **`listingscodes.csv`** — 3,818 latitude/longitude coordinate pairs extracted from the listings, used to test the ZIP-code conversion workflow.
* **`AirbnbMarketAnalysis.twbx`** — The packaged Tableau workbook containing the interactive dashboard.

## Lat/Long to ZIP Code Converter

`latlon_to_zipcode.py` maps latitude/longitude coordinates to approximate ZIP codes using the `pgeocode` library, which bundles postal-code data from GeoNames (downloaded once, then cached locally; no API keys required). ZIP codes are assigned by finding the nearest postal-area centroid to each coordinate using the haversine (great-circle) distance.

### Installation

```bash
python3 -m pip install pgeocode
```

### Usage from the command line

Place the script and your CSV (containing `latitude` and `longitude` columns) in the same folder, then run:

```bash
python3 latlon_to_zipcode.py listingscodes.csv
```

This reads `listingscodes.csv` and writes `listingscodes_with_zipcodes.csv` with a new `zipcode` column appended.

Options:

| Flag | Description | Default |
|------|-------------|---------|
| `-lat` / `-lon` | Column names holding latitude and longitude | `latitude`, `longitude` |
| `-o` | Output CSV path | `<input>_with_zipcodes.csv` |
| `-c` | Two-letter country code | `us` |
| `-d` | Only assign a ZIP when the nearest postal area is within this many km (otherwise left blank) | unlimited |

### Example

```bash
python3 latlon_to_zipcode.py listingscodes.csv -d 200
```

```
Processed 3,818 rows -> 3,818 ZIP codes assigned
Output written to: listingscodes_with_zipcodes.csv
```

These generated ZIP codes feed into the geographic comparisons used by the Tableau dashboard. Because ZIPs are matched to postal-area centroids, coordinates near ZIP borders may map to an adjacent ZIP, which is appropriate for ZIP-code-level market analysis.

### Using the Python functions directly

* `coords_to_zip(latitude, longitude)` — return the ZIP for a single point.
* `coords_to_zips(latitudes, longitudes)` — return ZIPs for lists of coordinates.
* `add_zipcodes(df, lat_col, lon_col)` — add a `zipcode` column to a pandas DataFrame.

## Results

The project resulted in an **interactive, multi-view Tableau dashboard** that provides a consolidated way to explore more than 12,000 Airbnb listings across the United States.

The dashboard enables users to investigate several dimensions of the Airbnb market, including:

* **Pricing Patterns** — Explore how listing prices differ across locations and different types of Airbnb properties.
* **Property & Room Types** — Compare the distribution of different property and room categories across the analyzed listings.
* **Geographic Distribution** — Examine where Airbnb listings are concentrated and compare market characteristics across approximate ZIP codes.
* **Host Characteristics** — Explore host-related information and its relationship to the overall listing landscape.
* **Availability** — Analyze calendar availability information to understand differences in listing availability across the dataset.
* **Customer Reviews** — Examine review-related metrics to understand patterns in customer activity across listings and markets.

The interactive nature of the dashboard allows users to filter and explore the data from different perspectives instead of relying on predetermined conclusions. This makes the analysis useful for identifying **location-level differences, pricing patterns, property distributions, and review trends** within the U.S. Airbnb market.

## Recommendations

The current dashboard provides a strong foundation for exploratory analysis, but the project could be extended with additional analytical techniques and data sources.

* **Seasonal Trend Analysis** — Analyze pricing and availability across different periods to identify seasonal patterns and determine when specific markets experience changes in listing activity.
* **Competitor Pricing Benchmarks** — Compare prices between similar property and room types within the same geographic areas to better understand relative pricing and market positioning.
* **Market-Level Comparisons** — Develop additional metrics for comparing ZIP codes or broader geographic markets based on pricing, listing density, availability, and review activity.
* **Host & Listing Performance Analysis** — Incorporate additional listing and host attributes to investigate which characteristics are associated with higher levels of customer engagement or review activity.
* **Demand & Pricing Forecasting** — Extend the project with forecasting techniques to estimate future pricing and availability trends across different markets.
* **Additional Data Sources** — Combine the Airbnb dataset with external geographic or market-level information to provide additional context when comparing different locations.

These extensions could move the project beyond descriptive visualization toward more advanced **market analysis, benchmarking, and predictive analytics**.
