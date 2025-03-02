# NVD_CVE_API_Project

# CVE Data Fetching and Visualization System

## Overview
This project is a **Python-based system** that fetches **CVE (Common Vulnerabilities and Exposures) data** from the **NVD API**, stores it in a **database**, and provides a **web-based UI** for users to query and visualize the data. Refer to the report for the detailed explanation and results

## Features
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

### 🚀 Steps to Implement

### **1️⃣ Fetch and Store CVE Data in a Database**
- Use **requests** to fetch CVE data from the **NVD API**.
- Implement **pagination** (`startIndex` and `resultsPerPage`) to retrieve all records.
- Store data in **MySQL**.
- Ensure **data cleansing and deduplication**.

### **2️⃣ Implement Periodic Data Sync**
- Perform **full refresh**

### **3️⃣ Develop a Flask Backend with Filtering APIs**
Expose REST APIs for querying CVE details based on:
- **CVE ID** → `/cves/{cve_id}`
- **Year** → `/cves/year/{year}`
- **CVE Score** → `/cves/score/{min_score}/{max_score}`
- **Last Modified** → `/cves/last-modified/{days}`

### **4️⃣ Build the UI with HTML**
- Use **Flask** to serve templates.
- Display CVE data in an **HTML table with AJAX**.
- Implement:
  - ✅ **Pagination**
  - ✅ **Sorting (Date column)**
  - ✅ **Clickable rows to view CVE details**

### **5️⃣ Documentation & Testing**
- **API Documentation:** Auto-generated with Swagger.
- **Unit Tests:** Using `pytest`.

---

## 📌 Installation & Setup

### **1️⃣ Clone the Repository**

git clone https://github.com/gnanithag5/NVD_CVE_API_Project
cd cve-visualizer

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
(http://127.0.0.1:5000/api/cve/id?cve_id=CVE-2023-1234 (Replace CVE-2023-1234 with an actual CVE ID from your database)) 
Returns details of a specific CVE.

---

## 3️⃣ Get CVEs by Year
(http://127.0.0.1:5000/api/cve/year?year=2023 (Replace 2023 with a year from your database)
) 
Returns CVEs from a specific year.

---

## 4️⃣ Get CVEs by Score
http://127.0.0.1:5000/api/cve/score?score=7.0 (Replace 7.0 with a score from your database) 
Filters CVEs with a **CVSS base score** above a threshold.

---

## 5️⃣ Get Recently Modified CVEs
http://127.0.0.1:5000/api/cve/modified?days=30 (This will return CVEs modified in the last 30 days)
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
