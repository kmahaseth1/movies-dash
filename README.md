# Movie Analytics Dashboard (WIP)

An interactive analytics dashboard built with Dash and Plotly to explore movie data from 2020s. This dashboard provides comprehensive insights into movie trends and performance through interactive visualizations and key performance indicators.

## Project Overview

This dashboard analyzes movie data from this decade, offering users the ability to explore various aspects of the film industry including box office performance, genre trends, release patterns, and audience ratings. The application features a clean, modern interface with responsive design and interactive elements.

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
- Data Correction:
    - Extract Production Country and Language from Wikipedia API

### TODO

- [ ] Write an API to extract data from the-numbers.com
- [ ] Extract budget and total gross data from the-numbers.com
- [ ] Integrate data from Wikipedia and the-number.com into the database table
- [ ] Deploy to production environment

## Dashboard Features

### Key Performance Indicators (KPIs)
- Total movies released
- Average box office revenue
- Top-performing movies
- Audience rating trends
- Release frequency by year

### Interactive Charts
- Top 10 Grossers
- Genre Distribution of Releases
- Budget Distribution by Year
- Comparison of revenue with audience ratings

### Filtering
- Year
- Genre
- Movie Type
- Production country

## Technical Stack

- Framework: Dash
- Visualization: Plotly
- Data Processing: Pandas, NumPy
- Data Source: The Movie Database (TMDB) API
