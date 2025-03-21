# NVD_CVE_API_Project

# CVE Data Fetching and Visualization System

## Overview
This project is a **Python-based system** that fetches **CVE (Common Vulnerabilities and Exposures) data** from the **NVD API**, stores it in a **database**, and provides a **web-based UI** for users to query and visualize the data. Refer to the report for the detailed explanation and results

### Features
✅ Fetch CVE data from the **NVD API**  
✅ Store data in **MySQL** 
✅ Periodic data sync 
✅ Backend API for CVE queries  
✅ Web-based **UI** for filtering and visualization  
✅ **Pagination, sorting, and search functionality**  

---

### 🛠 Technology Stack
- **Backend:** Python, Flask 
- **Database:** MySQL
- **Frontend:** HTML
- **Testing:** Pytest, Unittest  
- **Deployment:** Docker (Optional)  

---

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd cve_project
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure the database:**
    * Create a MySQL database and update `config.py` with your database credentials (DB\_HOST, DB\_USER, DB\_PASSWORD, DB\_NAME).
    * Execute the `mysql_code.sql` script to create the database schema.
4.  **Run the application:**
    ```bash
    python main.py --all
    ```

### Functionality

* **Data Fetching:** Fetches CVE data from the NVD API and stores it in a MySQL database.
* **Database Management:** Manages the MySQL database, including data cleaning and validation.
* **API:** Provides API endpoints to access CVE data.
* **Web UI:** A basic web interface to display and search CVE data.
* **Unit Tests:** Tests to ensure functionality.
* **Centralized Execution:** A `main.py` script to orchestrate execution.

### API Endpoints

* **Get CVE Filter Data Web UI:** `http://127.0.0.1:5000/`
* To get foltered data separately use the following endpoints.
* **Get CVE by ID:** `http://127.0.0.1:5000/api/cve/id?cve_id=CVE-XXXX-YYYY`
* **Get CVEs by Year:** `http://127.0.0.1:5000/api/cve/year?year=YYYY`
* **Get CVEs by Score:** `http://127.0.0.1:5000/api/cve/score?score=X.X`
* **Get Recently Modified CVEs:** `http://127.0.0.1:5000/api/cve/modified?days=N`

### Web UI

* **CVE List:** `http://127.0.0.1:5000/cves/list?page=1&resultsPerPage=10`
    * Allows pagination and searching.
    * Displays CVE details when clicked.

### Execution

* Run `python main.py --all` to execute all scripts in order: database setup, data fetching, API server, web UI server, and unit tests.

### Configuration

* Edit `config.py` to adjust database credentials, API URL, results per page, logging level, and log file path.

### Troubleshooting

**MySQL Connection Errors:**

* Verify database credentials in `config.py`.
* Confirm the MySQL server is running.

**API Issues:**

* Ensure all dependencies are installed (`pip list`).
* Verify the Flask API (`api_fetch.py`) is running.

## Future Work

* **Incremental Synchronization:** Implement incremental CVE data updates instead of full synchronizations to improve efficiency and reduce data fetching time. This would involve tracking the last updated CVE and only fetching changes since that point.
* **Periodic Synchronization:** Explore and implement periodic full synchronizations using third-party scheduling modules to ensure data integrity and catch any missed updates.

