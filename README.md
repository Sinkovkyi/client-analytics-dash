# Project: Website Data Visualization

This project aims to visualize website client data, including country distribution and cumulative revenue over time.

## Data

The following data points are used for visualization:

* **Date**: The date the client visited the website.
* **Country**: The country where the client is located.
* **Target**: The amount of money this client brought to the company.

## Graphical Components

The visualization will include the following graphical parts:

* A page with a time filter, allowing selection of data by monthly intervals.
* A Pie Chart displaying the distribution of clients by country, excluding invalid values.
* Cumulative revenue per country, presented as multiple charts. The x-axis of these charts will represent days from the selected time filter.

## Requirements

* There are no special hosting requirements; the page can be hosted on a local server.
* Dynamic interaction is preferred: charts should update and reload automatically when filters are changed.

## Final Output

The expected final output for this project includes:

* A Python script.
* A 2-minute video (screen recording) demonstrating the functionality of the visualization.

## How to Run

```bash
pip install -r requirements.txt
python app.py
