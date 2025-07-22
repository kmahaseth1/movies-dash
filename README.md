# Movie Analytics Dashboard (WIP)

An interactive analytics dashboard built with Dash and Plotly to explore American movie data from 2020s. This dashboard provides comprehensive insights into movie trends and performance through interactive visualizations and key performance indicators.

## Project Overview

This dashboard analyzes movie data from this decade for movies produced in the United States, offering users the ability to explore various aspects of the film industry including box office performance, genre trends, release patterns, and audience ratings. The application features a clean, modern interface with responsive design and interactive elements.

## Current Status

**Work in Progress** - The dashboard is currently under development with the following status:

### Completed Features
- KPI Cards: Key performance indicators with proper formatting and styling
- Chart Components: All visualization components are styled and formatted
- Layout Design: Complete dashboard layout with responsive grid system
- UI/UX: Modern, professional styling and component design
- Interactivity: Charts and KPIs update based on filters via Dash callbacks
- Full Data Integration: Includes all movies with complete data from 2020s present in the TMDB

### In Progress
- Final UI Changes (Assign colors to genres for the bar chart, make movie name font size on KPI cards dynamic)

### TODO
- [ ] Add a data dictionary or similar document
- [ ] Deploy to production environment

## Dashboard Features

### Key Performance Indicators (KPIs)
- Highest Grossing Movie
- Leading Genre
- Total Cumulative Revenue
- Total Movies

### Interactive Charts
- Top 10 Grossers
- Genre Distribution of Releases
- Budget Distribution by Year
- Comparison of revenue with audience ratings

### Filtering
- Year
- Genre
- Movie Type

## Technical Stack

- Framework: Dash
- Visualization: Plotly
- Data Processing: Pandas, NumPy
- Data Sources: The Movie Database (TMDB) API and Wikipedia API
- Deployment Platform: Render

## Resources

1. [Real Python Dash Tutorial](https://realpython.com/python-dash/): Very helpful manual on building simple dashboards using Dash and Plotly
2. [Plotly Express Documentation](https://plotly.com/python/plotly-express/): Good reference on creating different charts using the Plotly Express API
3. Chapter 17 of *Python Crash Course* by Eric Matthes (3rd ed.): Useful tutorial on working with web APIs to extract data and using Plotly to visualize them
4. Chapter 7 of *Automate the Boring Stuff with Python* by Al Sweigart (2nd ed.): Informative guide on applying regular expressions to accurately extract specific string patterns from text data