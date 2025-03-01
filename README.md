# NVD_CVE_API_Project

# CVE Data Fetching and Visualization System

## Overview
This project is a **Python-based system** that fetches **CVE (Common Vulnerabilities and Exposures) data** from the **NVD API**, stores it in a **database**, and provides a **web-based UI** for users to query and visualize the data. Refer to the report for the detailed explanation and results

## Features
✅ Fetch CVE data from the **NVD API**  
✅ Store data in **MySQL** or **MongoDB**  
✅ Periodic data sync using **Celery**  
✅ Backend API for CVE queries  
✅ Web-based **UI** for filtering and visualization  
✅ **Pagination, sorting, and search functionality**  

---

## 🛠 Technology Stack
- **Backend:** Python, Flask, Celery (for periodic tasks)  
- **Database:** MySQL / PostgreSQL / MongoDB  
- **Frontend:** HTML, CSS, JavaScript (Fetch API for AJAX)  
- **Testing:** Pytest, Unittest  
- **Deployment:** Docker (Optional)  

---

## 🚀 Steps to Implement

### **1️⃣ Fetch and Store CVE Data in a Database**
- Use **requests** to fetch CVE data from the **NVD API**.
- Implement **pagination** (`startIndex` and `resultsPerPage`) to retrieve all records.
- Store data in **MySQL** or **MongoDB**.
- Ensure **data cleansing and deduplication**.

### **2️⃣ Implement Periodic Data Sync**
- Use **Celery with Redis** or a **cron job** for periodic updates.
- Perform **full or incremental refresh** based on the last modified date.

### **3️⃣ Develop a Flask Backend with Filtering APIs**
Expose REST APIs for querying CVE details based on:
- **CVE ID** → `/cves/{cve_id}`
- **Year** → `/cves/year/{year}`
- **CVE Score** → `/cves/score/{min_score}/{max_score}`
- **Last Modified** → `/cves/last-modified/{days}`

### **4️⃣ Build the UI with HTML, CSS, and JavaScript**
- Use **Flask** to serve templates.
- Display CVE data in an **HTML table with AJAX**.
- Implement:
  - ✅ **Pagination**
  - ✅ **Sorting (Date column)**
  - ✅ **Clickable rows to view CVE details**

### **5️⃣ Documentation & Testing**
- **API Documentation:** Auto-generated with Swagger.
- **Unit Tests:** Using `pytest`.
- **Security:** Validate inputs & prevent SQL injection.

---

## 📌 Installation & Setup

### **1️⃣ Clone the Repository**

git clone https://github.com/gnanithag5/NVD_CVE_API_Project
cd cve-visualizer

## Project Structure

NVD_CVE_API_Project/
│── app2.py                # Main Flask application to integrate the frontend
│── fetch_CVE_data.py      # Fetches CVE data from NVD API
│── full_syn.py            # Synchronizes data periodically
│── api_fetch.py           # API for filtering CVEs
│── database.py            # DB connection logic
│── mysql_code.sql         # Defines database schema
│── requirements.txt       # Dependencies for the project
│
├── templates/             # HTML templates
│   ├── cve_list.html      # Displays CVE list in a table
│   ├── cve_detail.html    # Shows details of a selected CVE
│
├── tests/                 # Contains unit tests
│   ├── unit_tests.py      # Unit tests for API & database
│
├── .pytest_cache/
    ├── CACHEDIR.TAG
    ├── .gitignore             # Specifies files to ignore in Git
    ├── README.md              # Project overview & instructions
    ├── venv/
    ├── v/

## CVE API Documentation

## Available Endpoints

### 1. Get all CVEs
**GET** `/api/cves`
Returns a list of all CVEs stored in the database.

### 2. Get CVE by ID
**GET** `/api/cves/{cve_id}`
Returns details of a specific CVE.

### 3. Get CVEs by Year
**GET** `/api/cves?year=2023`
Filters CVEs based on the year.

### 4. Get CVEs by Score
**GET** `/api/cves?min_score=7.0`
Filters CVEs with a score above a threshold.

## 🔗 Available API Endpoints

## 1️⃣ Get All CVEs
**GET** `/api/cves`  
Returns all stored CVEs.

---

## 2️⃣ Get CVE by ID
**GET** `/api/cve/id?cve_id=CVE-2023-1234`  
Returns details of a specific CVE.

---

## 3️⃣ Get CVEs by Year
**GET** `/api/cve/year?year=2023`  
Returns CVEs from a specific year.

---

## 4️⃣ Get CVEs by Score
**GET** `/api/cve/score?score=7.0`  
Filters CVEs with a **CVSS base score** above a threshold.

---

## 5️⃣ Get Recently Modified CVEs
**GET** `/api/cve/modified?days=30`  
Fetches CVEs modified in the last **N** days.


## Setup Guide

### 1. Install Dependencies from requirements.txt
### 2. Connect Mysql using database.py with the sql schema available in mysql_code.sql
### 3. Run fetch_CVE_data.py for fetching data
### 4. Run full_sync.py for synchronizing the data
### 5. Run api_fetch.py for filtering
### 6. Run app2.py for UI
### 7. Run unit_tests.py for testing

# 🛠 Technologies Used  
- **Python (Flask)**  
- **MySQL** (pymysql, mysql-connector)  
- **HTML (Jinja templates)**  

---

## ❗ Troubleshooting  

## 1️⃣ MySQL connection errors?  
- Check `database.py` for correct credentials.  
- Ensure MySQL server is running.  

## 2️⃣ API not running?  
- Check dependencies with `pip list`.  
- Ensure Flask is installed and `api_fetch.py` is executed.  

---

## 📄 License  
This project is open-source under the **MIT License**.  
