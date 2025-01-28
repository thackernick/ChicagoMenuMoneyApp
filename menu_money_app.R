# Load libraries
library(tidyverse)
library(tidygeocoder)
library(dplyr)
library(ggplot2)
library(shiny)
library(leaflet)
library(bslib)
library(plotly)

# Load the dataset
menu_data <- read.csv("AllMenu2012-2023_geocoded_full.csv")

menu_data <- menu_data[!is.na(menu_data$latitude) & !is.na(menu_data$longitude), ]


menu_data <- menu_data[menu_data$cost >= 0, ]

# UI
ui <- fluidPage(
  theme = bs_theme(bootswatch = "lux"),
  titlePanel(div(
    style = "text-align: center;",
    h1("Chicago Menu Money Expenditures", style = "color: #2c3e50; font-weight: bold;"),
    h5("Explore how your ward's menu money was spent over the years", style = "color: #7f8c8d;")
  )),
  
  div(
    style = "display: flex; flex-direction: row;",
    div(
      style = "background-color: #ecf0f1; border-radius: 10px; padding: 10px; width: 250px; margin-right: 20px;",
      selectInput(
        inputId = "year",
        label = "Select Year:",
        choices = sort(unique(menu_data$year)),
        selected = max(menu_data$year, na.rm = TRUE)
      ),
      selectInput(
        inputId = "ward",
        label = "Select Your Ward:",
        choices = sort(unique(menu_data$ward)),
        selected = 1
      ),
      tags$hr(),
      p("Each Chicago ward receives $1.5 million annually for capital improvements.", style = "font-size: 12px; color: #2c3e50;")
    ),
    div(
      style = "flex-grow: 1;",
      leafletOutput("map", width = "100%", height = "700px"),
      h4("Spending Breakdown by Category", style = "color: #2c3e50; margin-top: 20px;"),
      plotlyOutput("category_plot")
    )
  )
)

# Server
server <- function(input, output) {
  # Reactive data for selected year and ward
  filtered_data <- reactive({
    filter(menu_data, year == input$year, ward == input$ward)
  })
  
  # Render map
  output$map <- renderLeaflet({
    data <- filtered_data()
    
    leaflet(data) %>%
      addTiles() %>%
      addCircleMarkers(
        lng = ~longitude,
        lat = ~latitude,
        popup = ~paste(
          "<b>Description:</b>", description,
          "<br><b>Category:</b>", category,
          "<br><b>Program:</b>", program,
          "<br><b>Cost:</b> $", format(cost, big.mark = ",", scientific = FALSE)
        ),
        radius = ~sqrt(cost) / 500,
        color = "#3498db",
        fillOpacity = 0.7
      )
  })
  
  # Render spending breakdown plot
  output$category_plot <- renderPlotly({
    data <- filtered_data() %>%
      group_by(category) %>%
      summarize(total_cost = sum(cost, na.rm = TRUE))
    
    p <- ggplot(data, aes(x = reorder(category, -total_cost), y = total_cost, fill = category, text = paste("Total Cost: $", scales::comma(total_cost)))) +
      geom_bar(stat = "identity", show.legend = FALSE) +
      coord_flip() +
      theme_minimal() +
      theme(
        text = element_text(color = "#2c3e50"),
        axis.title = element_text(size = 14, face = "bold"),
        axis.text = element_text(size = 12),
        plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
        panel.grid = element_blank()
      ) +
      labs(
        title = paste("Spending Breakdown for Ward", input$ward, "in", input$year),
        x = "Category",
        y = "Total Cost ($)"
      ) +
      scale_y_continuous(labels = scales::comma)
    
    ggplotly(p, tooltip = "text")
  })
}

# Run the app
shinyApp(ui = ui, server = server)

