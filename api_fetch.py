from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime

app = Flask(__name__)

# MySQL connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nani@2001",
        database="cve_database"
    )

# Route to filter CVE details by CVE ID
@app.route('/api/cve/id', methods=['GET'])
def get_cve_by_id():
    cve_id = request.args.get('cve_id', None)
    if not cve_id:
        return jsonify({"error": "CVE ID is required"}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM cve_data WHERE cve_id = %s', (cve_id,))
    cve_data = cursor.fetchone()
    cursor.close()
    db.close()

    if cve_data:
        return jsonify(cve_data)
    else:
        return jsonify({"error": "CVE ID not found"}), 404

# Route to filter CVE details by specific year
@app.route('/api/cve/year', methods=['GET'])
def get_cve_by_year():
    year = request.args.get('year', None)
    if not year:
        return jsonify({"error": "Year is required"}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM cve_data WHERE YEAR(lastModified) = %s', (year,))
    cve_data = cursor.fetchall()
    cursor.close()
    db.close()

    if cve_data:
        return jsonify(cve_data)
    else:
        return jsonify({"error": "No CVEs found for the given year"}), 404

# Route to filter CVE details by CVE Score (CVSS base score)
@app.route('/api/cve/score', methods=['GET'])
def get_cve_by_score():
    score = request.args.get('score', None)
    if not score:
        return jsonify({"error": "Score is required"}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM cve_data WHERE metrics.cvssMetricV3.cvssData.baseScore >= %s', (score,))
    cve_data = cursor.fetchall()
    cursor.close()
    db.close()

    if cve_data:
        return jsonify(cve_data)
    else:
        return jsonify({"error": "No CVEs found with the given score"}), 404

# Route to filter CVE details by last modified date in N days
@app.route('/api/cve/modified', methods=['GET'])
def get_cve_by_modified():
    try:
        days = int(request.args.get('days', 0))
    except ValueError:
        return jsonify({"error": "Invalid number of days"}), 400

    if days <= 0:
        return jsonify({"error": "Days must be a positive integer"}), 400

    date_n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM cve_data WHERE lastModified >= %s', (date_n_days_ago,))
    cve_data = cursor.fetchall()
    cursor.close()
    db.close()

    if cve_data:
        return jsonify(cve_data)
    else:
        return jsonify({"error": "No CVEs found modified in the last N days"}), 404

if __name__ == '__main__':
    app.run(debug=True)
