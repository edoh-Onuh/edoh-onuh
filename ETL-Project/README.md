# ETL Project

This script performs an ETL (Extract, Transform, Load) process for customer and employee data from various file formats (CSV, JSON, XML, TXT) into a MySQL database.

**Note:** This project was completed as a school assignment using provided sample data files.

## Prerequisites

- Python 3.x
- MySQL Server

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Configuration:**
    - Ensure your MySQL server is running.
    - Create a database.
    - Update the database connection details in `etl_script.py`:
      ```python
      db.bind(
          provider='mysql',
          host='127.0.0.1',
          port=3306,
          user='your_mysql_user',
          password='your_mysql_password',
          database='your_database_name'
      )
      ```

5.  **Data Files:**
    Place the following data files in the same directory as the `etl_script.py`:
    - `customers.csv`
    - `customers_subscriptions.json`
    - `customers_billing.xml`
    - `employees.csv`
    - `employees_vehicles.xml`
    - `employees_salaries.json`
    - `flagged_prompts.txt`

## Running the Script

Execute the script from your terminal:
```bash
python etl_script.py
```
The script will connect to the database, process the files, and load the data into the `Customer` and `Employee` tables.

