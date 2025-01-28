# Democratizing Chicago's Menu Money Data

Parsing, cleaning, geocoding, and visualizing Chicago's menu money expenditures with Python and R.

## Description

Each year, every member of Chicago's city council is allocated $1.5 million in "menu money" to fund capital improvements in their ward. These funds can be spent on streets, sidewalks, parks, lighting, and more. While this system gives alderpersons the flexibility to address local needs, it has also raised concerns about transparency and misuse. Historically, menu money expenditures have been published in large, unorganized PDFs, making it difficult for the public to understand how funds are allocated.

This project aims to:
1. **Geocoding**: Locations of expenditures are cleaned and geocoded using a Python script.
2. **Visualization**: A Shiny app in R provides an interactive tool to explore spending by ward, year, and category.
3. **Empowerment**: By making the data accessible, the project encourages public engagement, investigative reporting, and policy analysis.

---

## Features

### Geocoding (Python)
- A Python script (`Geocode.py`) processes and geocodes addresses using OpenCage.
- Handles inconsistencies in data (e.g., intersections or ranges like "FROM X TO Y").
- Saves geocoded results in a AllMenu2012-2023_geocoded_full.csv for use in further analysis.

### Interactive Web App (R Shiny)
- Explore how each ward allocates menu money through a dynamic and user-friendly interface.
- Key Features:
  - Interactive map showing expenditures by category and location.
  - Visualizations (bar chart) summarizing spending trends.
  - Filter by ward, year, or category for detailed insights.

---

## Getting Started

### Prerequisites
- **R** (version 4.0 or higher recommended)
- **RStudio** (optional but recommended)
- R packages: `shiny`, `dplyr`, `ggplot2`, `leaflet`, `DT`, `readr`, `tidyr`, etc.

### Files in this Repository
1. **`Geocode.py`**:
   - Python script for geocoding menu money data.
2. **`menu_money_app.R`**:
   - Shiny app for visualizing menu money expenditures.
3. **`AllMenu2012-2023_geocoded_full.csv`**:
   - Geocodes addresses using OpenStreetMap

---

## Running the Project

### Access the Shiny App
You can access the interactive web app here:  
**[Chicago Menu Money Visualization App](https://ragtimefed.shinyapps.io/chicagomenuapp/)**


### Running the Shiny App Locally

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/ChicagoMenuMoneyApp.git


# Credits
Original methodology and code by [Jake J. Smith](http://www.jakejsmith.com) & [Andres Fonseca](https://github.com/fonsecaa) Python geocoding and Shiny app integration by contributors.
