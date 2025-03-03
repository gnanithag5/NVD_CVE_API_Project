import mysql.connector
import requests
import time
import config
import json

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def fetch_cve_data(start_index):
    """Fetch CVE data from the NVD API with pagination."""
    params = {
        "resultsPerPage": config.RESULTS_PER_PAGE,
        "startIndex": start_index
    }
    print(f"Fetching CVE data (startIndex={start_index})...")

    try:
        response = requests.get(config.API_URL, params=params)
        response.raise_for_status()
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Raw API Response: {response.text[:500]}")

        try:
            json_data = response.json()
            vulnerabilities = json_data.get("vulnerabilities", [])
            total = json_data.get("totalResults", 0)
            print(f"Retrieved {len(vulnerabilities)} CVEs (Total Available: {total})")
            return vulnerabilities, total
        except json.JSONDecodeError:
            print("Error decoding JSON response from API.")
            return [], 0

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return [], 0

def insert_cve_data(cve_list, cursor):
    """Insert fetched CVE data into MySQL database."""
    if not cve_list:
        print("No CVE data to insert.")
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
            description = next((desc["value"] for desc in cve.get("descriptions", []) if desc["lang"] == "en"), "No description available")

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

            sql = """
                INSERT INTO cve_data (cve_id, source_identifier, published_date, last_modified_date, vuln_status, description, 
                base_score, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, availability_impact)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE last_modified_date=VALUES(last_modified_date), description=VALUES(description);
            """

            values = (cve_id, source_identifier, published_date, last_modified_date, vuln_status, description,
                      base_score, access_vector, access_complexity, authentication,
                      confidentiality_impact, integrity_impact, availability_impact)

            cursor.execute(sql, values)
            inserted_count += 1

        except mysql.connector.Error as err:
            print(f"Error inserting CVE {cve_id}: {err}")

    print(f"Inserted {inserted_count} CVE records into MySQL.")

def main():
    """Main execution function with incremental commits."""
    print("Starting CVE data fetch and storage process...")
    db = get_db_connection()
    if db is None:
        return
    cursor = db.cursor()

    start_index = 0
    batch_size = 100 #Commit after every 100 insertions. You can change this.
    inserted_count = 0

    try:
        while True:
            cve_data, total_results = fetch_cve_data(start_index)
            if not cve_data:
                print("No more CVE records to fetch. Exiting.")
                break

            insert_cve_data(cve_data, cursor)
            inserted_count += len(cve_data)

            if inserted_count >= batch_size:
                db.commit()
                print(f"Committed {inserted_count} CVE records.")
                inserted_count = 0

            start_index += config.RESULTS_PER_PAGE
            if start_index >= total_results:
                print("All available CVEs have been fetched.")
                break

            print(f"Waiting before fetching the next batch (startIndex={start_index})...")
            time.sleep(5)

        # Commit any remaining records
        if inserted_count > 0:
            db.commit()
            print(f"Committed remaining {inserted_count} CVE records.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()

    finally:
        cursor.close()
        db.close()
        print("Data fetching and storage process completed.")

if __name__ == "__main__":
    main()