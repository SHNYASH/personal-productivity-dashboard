# **Personal Productivity Dashboard**

## **Project Overview**
This project is an automated ETL pipeline designed to analyze personal productivity data. 
It extracts event details from one or multiple google calendars, transforms the data and 
loads it into a PostgreSQL database, from where it can be later used to build a productivity
dashboard in PowerBI or any other visualization software.

## **Tech Stack**
Language: Python 3.11.9
Database: PostgreSQL
APIs: Google Calendar API
Libraries: Pandas, SQLAlchemy

## **Project Structure**
The ETL logic is separated into 3 different scripts with distinct functionalities.

Extract.py: Establishes connection to the API and extracts events data from one or multiple google calendars.
Transform.py: Cleans the extracted data using Pandas.
Load.py: Connects to the PostgreSQL database via SQLAlchemy and upserts data into the staging table to ensure integrity.

Inside the database, the selected events data is combined with a separate dates table and displayed as a "productivity" view.
This view is later imported into PowerBI, where limited data transformation happens, and new measures are created. The information
is then displayed on 2 pages:

Overview: Contains the main visuals for the entire time period of imported events with an option to narrow the time window by using a slider.

<img src="Overview%20Page.png" width="600">

Weekly: Contains visuals that display events information only for the current week, making it useful for week-on-week comparison.

<img src="Weekly%20Page.png" width="600">

## **Setup Instructions**
    1. Clone the Repository
            git clone https://github.com/SHNYASH/personal-productivity-dashboard
    2. Install Dependencies
            pip install -r requirements.txt
    3. Configuration
            Add your google cloud credentials file to the working folder to authorize google calendar API access.
            Create a .env file in the root directory and add your PostgreSQL credentials:
            DB_USER=your_user
            DB_PASS=your_password
            DB_HOST=localhost
            DB_PORT=5432
            DB_NAME=your_db
    4. Database Setup 
            Setup the database schema using .sql files stored in the SQL folder. Note: Do not change the names of columns, views, or tables.
    5. Run the Pipeline
            python Run.py
    6. Dashboard Setup
            Open the Personal Productivity Dashboard.pbix and connect PowerBI to your database.

 
