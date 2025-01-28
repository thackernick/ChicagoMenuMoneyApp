# Democratizing Chicago's Menu Money Data

Parsing, cleaning, geocoding, and visualizing Chicago's menu money expenditures with Python and R.

## Description

Each year, every member of Chicago's city council is allocated $1.5 million in "menu money" to fund capital improvements in their ward. These funds can be spent on streets, sidewalks, parks, lighting, and more. While this system gives alderpersons the flexibility to address local needs, it has also raised concerns about transparency and misuse. Historically, menu money expenditures have been published in large, unorganized PDFs, making it difficult for the public to understand how funds are allocated.

This project aims to change that:
1. **Geocoding**: Locations of expenditures are cleaned and geocoded using a Python script.
2. **Visualization**: A Shiny app in R provides an interactive tool to explore spending by ward, year, and category.
3. **Empowerment**: By making the data accessible, the project encourages public engagement, investigative reporting, and policy analysis.

---

## Features

### Geocoding (Python)
- A Python script (`menu_money_geocode.py`) processes and geocodes addresses using OpenStreetMap.
- Handles inconsistencies in data (e.g., intersections or ranges like "FROM X TO Y").
- Saves geocoded results in a CSV for use in further analysis.

### Interactive Web App (R Shiny)
- Explore how each ward allocates menu money through a dynamic and user-friendly interface.
- Key Features:
  - Interactive map showing expenditures by category and location.
  - Visualizations (e.g., bar charts, pie charts) summarizing spending trends.
  - Filter by ward, year, or category for detailed insights.

---

## Getting Started

### Prerequisites
- **Python**:
  - Install the required packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
- **R/R Studio**:
  - Ensure the following R packages are installed:
    - `shiny`
    - `tidyverse`
    - `leaflet`
    - `ggplot2`
    - `sf`

### Files in this Repository
1. **`menu_money_geocode.py`**:
   - Python script for geocoding menu money data.
2. **`menu_money_app.R`**:
   - Shiny app for visualizing menu money expenditures.
3. **`AllMenu2012-2023.csv`**:
   - Cleaned and categorized menu money dataset.
4. **`requirements.txt`**:
   - Python dependencies for geocoding.
5. **`README.md`**:
   - This document, detailing the project and its components.

---

## Running the Project

### Geocoding
1. Navigate to the directory containing `menu_money_geocode.py`.
2. Run the script:
   ```bash
   python menu_money_geocode.py



# Credits
Original methodology and code by [Jake J. Smith](http://www.jakejsmith.com) & [Andres Fonseca](https://github.com/fonsecaa) Python geocoding and Shiny app integration by contributors.
