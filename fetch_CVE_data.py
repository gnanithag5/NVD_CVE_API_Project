print("🚀 Script started!")

print("🌐 Attempting to fetch CVE data from API...")

import mysql.connector
import requests
import time

# MySQL Connection Setup
try:
    db = mysql.connector.connect(
        host="localhost",  # Change if MySQL is on another server
        user="root",
        password="Nani@2001",
        database="cve_database"
    )
    cursor = db.cursor()
    print("✅ Successfully connected to MySQL.")
except mysql.connector.Error as err:
    print(f"❌ Error connecting to MySQL: {err}")
    exit()

# NVD API Endpoint
API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Parameters for pagination
results_per_page = 2000  # Max allowed
start_index = 0  # Ensure this updates in each loop
total_results = None  # Will be updated after the first request


def fetch_cve_data(start_index):
    """Fetch CVE data from the NVD API with pagination."""
    params = {
        "resultsPerPage": results_per_page,
        "startIndex": start_index
    }
    print(f"🔄 Fetching CVE data (startIndex={start_index})...")

    response = requests.get(API_URL, params=params)
    print(f"HTTP Status Code: {response.status_code}")  # Debugging
    print("Raw API Response:", response.text[:500])  # Show first 500 chars for verification
    
    if response.status_code == 200:
        json_data = response.json()
        vulnerabilities = json_data.get("vulnerabilities", [])
        total = json_data.get("totalResults", 0)
        print(f"📦 Retrieved {len(vulnerabilities)} CVEs (Total Available: {total})")
        return vulnerabilities, total
    else:
        print(f"❌ Error fetching data: HTTP {response.status_code}")
        return [], 0


def insert_cve_data(cve_list):
    """Insert fetched CVE data into MySQL database."""
    if not cve_list:
        print("⚠️ No CVE data to insert.")
        return

    inserted_count = 0

    for item in cve_list:
        try:
            cve = item["cve"]
            cve_id = cve["id"]
            source_identifier = cve["sourceIdentifier"]
            published_date = cve["published"]
            last_modified_date = cve["lastModified"]
            vuln_status = cve["vulnStatus"]
            
            # Extract first English description
            descriptions = cve.get("descriptions", [])
            description = next((desc["value"] for desc in descriptions if desc["lang"] == "en"), "No description available")
            
            # Extract CVSS metrics if available
            metrics = cve.get("metrics", {}).get("cvssMetricV2", [])
            if metrics:
                cvss_data = metrics[0]["cvssData"]
                base_score = cvss_data["baseScore"]
                access_vector = cvss_data["accessVector"]
                access_complexity = cvss_data["accessComplexity"]
                authentication = cvss_data["authentication"]
                confidentiality_impact = cvss_data["confidentialityImpact"]
                integrity_impact = cvss_data["integrityImpact"]
                availability_impact = cvss_data["availabilityImpact"]
            else:
                base_score = access_vector = access_complexity = authentication = None
                confidentiality_impact = integrity_impact = availability_impact = None
            
            # Insert Data into MySQL
            sql = """
            INSERT INTO cve_data 
            (cve_id, source_identifier, published_date, last_modified_date, vuln_status, description, 
            base_score, access_vector, access_complexity, authentication, 
            confidentiality_impact, integrity_impact, availability_impact) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            last_modified_date=VALUES(last_modified_date), 
            description=VALUES(description);
            """
            
            values = (cve_id, source_identifier, published_date, last_modified_date, vuln_status, description, 
                      base_score, access_vector, access_complexity, authentication, 
                      confidentiality_impact, integrity_impact, availability_impact)
            
            cursor.execute(sql, values)
            inserted_count += 1

        except mysql.connector.Error as err:
            print(f"⚠️ Error inserting CVE {cve_id}: {err}")

    db.commit()
    print(f"✅ Inserted {inserted_count} CVE records into MySQL.")


# Main Execution
if __name__ == "__main__":
    print("🚀 Starting CVE data fetch and storage process...")

    start_index = 0  # Initialize start index before the loop

    while True:
        cve_data, total_results = fetch_cve_data(start_index)  # Use the updated start_index

        if not cve_data:
            print("🎉 No more CVE records to fetch. Exiting.")
            break

        insert_cve_data(cve_data)

        start_index += results_per_page  # Move to the next batch

        # Stop if we reached the total results count
        if start_index >= total_results:
            print("✅ All available CVEs have been fetched.")
            break

        print(f"⏳ Waiting before fetching the next batch (startIndex={start_index})...")
        time.sleep(5)  # To avoid API rate limits

    print("🚀 Data fetching and storage process completed.")
