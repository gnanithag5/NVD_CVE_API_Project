import pymysql

# MySQL connection details
MYSQL_USER = "root"
MYSQL_PASSWORD = "Nani@2001"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "cve_database"

# Connect to MySQL
conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    port=MYSQL_PORT
)

cursor = conn.cursor()

# Read and execute SQL file
with open("cve_database.sql", "r") as sql_file:  # Replace with your file name
    sql_script = sql_file.read()
    cursor.execute(sql_script)  # This runs your SQL schema and data

conn.commit()
cursor.close()
conn.close()

print("✅ Database setup completed successfully!")
