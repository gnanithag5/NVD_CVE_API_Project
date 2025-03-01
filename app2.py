from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection helper
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='Nani@2001', 
        database='cve_database'
    )
    return connection

@app.route('/cves/list', methods=['GET'])
def cve_list():
    results_per_page = int(request.args.get('resultsPerPage', 10))  # Default 10
    page = int(request.args.get('page', 1))  # Page number
    start_index = (page - 1) * results_per_page

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute('''SELECT cve_id, source_identifier, published_date, last_modified_date, vuln_status 
                      FROM cve_data LIMIT %s OFFSET %s''', (results_per_page, start_index))
    cve_data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('cve_list.html', cve_data=cve_data, results_per_page=results_per_page,
                           current_page=page)

    
@app.route('/cves/<cve_id>', methods=['GET'])
def cve_detail(cve_id):
    # Connect to the database
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Query to fetch all columns for the specific CVE ID
    cursor.execute('''SELECT cve_id, source_identifier, description, base_score, published_date, 
                      last_modified_date, vuln_status, access_vector, access_complexity, authentication, 
                      confidentiality_impact, integrity_impact, availability_impact 
                      FROM cve_data WHERE cve_id = %s''', (cve_id,))
    cve_data = cursor.fetchone()
    cursor.close()
    db.close()

    if cve_data:
        return render_template('cve_detail.html', cve_data=cve_data)
    else:
        return jsonify({"error": "CVE ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
