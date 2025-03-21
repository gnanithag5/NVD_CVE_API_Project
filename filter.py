from flask import Flask, render_template, request, jsonify
import mysql.connector
import datetime
import config

app = Flask(__name__)

def get_db_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

@app.route('/')
def home():
    """Renders the frontend page."""
    return render_template("index.html")  # Ensure index.html is in the "templates" folder

@app.route('/api/cve/id', methods=['GET'])
def get_cve_by_id():
    """Retrieves CVE details by CVE ID."""
    cve_id = request.args.get('cve_id', None)
    if not cve_id:
        return jsonify({"error": "CVE ID is required"}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cve_data WHERE cve_id = %s', (cve_id,))
        cve_data = cursor.fetchone()
        cursor.close()
        db.close()

        if cve_data:
            return jsonify(cve_data)
        else:
            return jsonify({"error": "CVE ID not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route('/api/cve/year', methods=['GET'])
def get_cve_by_year():
    """Retrieves CVE details by year."""
    year = request.args.get('year', None)
    if not year:
        return jsonify({"error": "Year is required"}), 400

    try:
        year = int(year)  # Convert year to integer
    except ValueError:
        return jsonify({"error": "Invalid year format. Must be an integer."}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cve_data WHERE YEAR(published_date) = %s', (year,))
        cve_data = cursor.fetchall()
        cursor.close()
        db.close()

        if cve_data:
            return jsonify(cve_data)
        else:
            return jsonify({"error": "No CVEs found for the given year"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route('/api/cve/score', methods=['GET'])
def get_cve_by_score():
    """Retrieves CVE details by score."""
    score = request.args.get('score', None)
    if not score:
        return jsonify({"error": "Score is required"}), 400

    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cve_data WHERE base_score >= %s', (score,))
        cve_data = cursor.fetchall()
        cursor.close()
        db.close()

        if cve_data:
            return jsonify(cve_data)
        else:
            return jsonify({"error": "No CVEs found with the given score"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.route('/api/cve/modified', methods=['GET'])
def get_cve_by_modified():
    """Retrieves CVE details modified in the last N days."""
    days = request.args.get('days', 0)
    if not days:
        return jsonify({"error": "Days is required"}), 400

    try:
        days = int(days)
    except ValueError:
        return jsonify({"error": "Invalid days format. Must be an integer."}), 400

    date_n_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cve_data WHERE last_modified_date >= %s', (date_n_days_ago,))
        cve_data = cursor.fetchall()
        cursor.close()
        db.close()

        if cve_data:
            return jsonify(cve_data)
        else:
            return jsonify({"error": "No CVEs found modified in the last N days"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
