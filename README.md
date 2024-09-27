# Data Extraction, Formatting, and Uploading System

This project implements a highly flexible data management system that can connect to a PostgreSQL database, execute queries, format the results, and upload the formatted data to various destinations.

## Primary Purpose
The primary purpose of this project is as a guerilla marketing tool for the sublease exchange company HostU. This tool can be used to extract listing data from the HostU database, format it into various types of social media posts, and then automatically upload those posts to their respective platforms. All that is required is a package with a new Formatter, Uploader, and DataManager Object.

The initial use is to create listing posts on facebook sublease exchange groups.

## Project Structure

The project consists of several Python modules:

- `Model/DataManager.py`: The main class that orchestrates the data processing workflow.
- `Model/Connection.py`: Handles database connections and query execution.
- `Model/Formatter.py`: Contains classes for formatting data (JSON and CSV).
- `Model/Uploader.py`: Provides classes for uploading formatted data to different destinations.

## Features

- Connect to PostgreSQL databases
- Execute custom SQL queries
- Format query results as JSON or CSV
- Upload formatted data to files, S3 buckets, or databases
- Configurable header inclusion in query results
- Save session attributes for later use
- Highly customizable for add-ons
  - New packages containing a new Formatter and 

## Requirements

- Python 3.x
- psycopg2 library for PostgreSQL connections

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/data-management-system.git
   ```

2. Install the required dependencies:
   ```
   pip install psycopg2
   ```

## Usage

Here's a basic example of how to use the DataManager class:
