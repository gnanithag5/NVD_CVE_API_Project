from flask import Flask, render_template, request, jsonify
import mysql.connector
import config

app = Flask(__name__)

# Database connection helper with error handling and context manager
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}") #basic error printing
        return None

@app.route('/cves/list', methods=['GET'])
def cve_list():
    results_per_page = int(request.args.get('resultsPerPage', 10))  # Default 10
    page = int(request.args.get('page', 1))  # Page number
    start_index = (page - 1) * results_per_page

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) FROM cve_data')
        total_records = cursor.fetchone()['COUNT(*)']

        cursor.execute('''SELECT cve_id, source_identifier, published_date, last_modified_date, vuln_status FROM cve_data LIMIT %s OFFSET %s''', (results_per_page, start_index))
        cve_data = cursor.fetchall()

        return render_template('cve_list.html', cve_data=cve_data, results_per_page=results_per_page, current_page=page, total_records=total_records)

    except mysql.connector.Error as e:
        print(f"Database query error: {e}") #basic error printing
        return jsonify({"error": "Database query error"}), 500

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

@app.route('/cves/<cve_id>', methods=['GET'])
def cve_detail(cve_id):
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute('''SELECT cve_id, source_identifier, description, base_score, published_date, last_modified_date, vuln_status, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, availability_impact FROM cve_data WHERE cve_id = %s''', (cve_id,))
        cve_data = cursor.fetchone()

        if cve_data:
            return render_template('cve_detail.html', cve_data=cve_data)
        else:
            return jsonify({"error": "CVE ID not found"}), 404

    except mysql.connector.Error as e:
        print(f"Database query error: {e}") #basic error printing
        return jsonify({"error": "Database query error"}), 500

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

#Input validation example.
@app.route('/cves/list_validated', methods=['GET'])
def cve_list_validated():
    try:
        results_per_page = int(request.args.get('resultsPerPage', 10))
        page = int(request.args.get('page', 1))

        if results_per_page <= 0 or page <= 0:
            return jsonify({"error": "Invalid parameters"}), 400

        start_index = (page - 1) * results_per_page

        db = get_db_connection()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) FROM cve_data')
        total_records = cursor.fetchone()['COUNT(*)']

        cursor.execute('''SELECT cve_id, source_identifier, published_date, last_modified_date, vuln_status FROM cve_data LIMIT %s OFFSET %s''', (results_per_page, start_index))
        cve_data = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('cve_list.html', cve_data=cve_data, results_per_page=results_per_page, current_page=page, total_records=total_records)

    except ValueError:
        return jsonify({"error": "Invalid parameter type"}), 400
    except mysql.connector.Error as e:
        print(f"database error: {e}")
        return jsonify({"error": "database error"}), 500

if __name__ == '__main__':
    app.run(debug=True)