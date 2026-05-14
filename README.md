- Project Overview -
This project is an end-to-end data pipeline designed to automate the extraction and analysis of hospital billing data. By connecting a MySQL database to Python, the script cleans raw patient records and generates high-level financial reports and visualizations to help a hospital’s revenue team identify collection risks and operational bottlenecks.

- Tech Stack -
Database: MySQL (Relational data storage)
Language: Python 3.x

Libraries:
Pandas & NumPy (Data manipulation)
SQLAlchemy & PyMySQL (Database connection)
Matplotlib & Seaborn (Data visualization)

- Key Features & Logic -
The script is organized into a 5-step pipeline:
Database Integration: Securely connects to a local MySQL instance and pulls live patient records into a Pandas DataFrame.
Data Cleaning: Standardizes column headers (removing spaces/caps) and identifies missing values to ensure data integrity.

Financial Metrics:
Calculates Total & Average Revenue.
Performs Portfolio Risk Segmentation by isolating high-value claims (>$30k) that represent significant financial exposure.

Operational Metrics:
Length of Stay (LOS): Calculates the duration of patient stays to monitor bed occupancy trends.
Revenue Per Day: A custom metric created to measure the financial yield of different medical conditions per hospitalized day.
Automated Reporting: Outputs six detailed text reports to the console and exports high-resolution charts for presentations.

- Visualizations -
The pipeline automatically generates the following insights:
Payer Performance: A bar chart comparing total revenue across different insurance providers.
Operational Efficiency: A horizontal chart showing which medical conditions require the longest hospital stays.

-Project Structure -
healthcare_revenue_cycle_analytics
├── main.py                          # Main Python script
├── README.md                        # Project documentation
├── healthcare_financial_dashboard

- Business Impact -
This tool replaces manual spreadsheet tracking. By automating the "Revenue at Risk" calculation, a hospital administrator can instantly see what percentage of the portfolio is tied up in high-value claims, allowing them to prioritize audits and improve cash flow.
