import pymysql
import config  # Import the config file

def setup_database():
    """Sets up the MySQL database by executing SQL from a file."""

    try:
        conn = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=3306  # Or config.DB_PORT if you add it to the config file.
        )
        cursor = conn.cursor()

        # Check if the database exists, and create it if not.
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME};")
        conn.commit()
        cursor.execute(f"USE {config.DB_NAME};")  # Select the database to use.

        with open("database/cve_database.sql", "r") as sql_file:
            sql_script = sql_file.read()
            # Execute each SQL command separately, in case there are multiple.
            for command in sql_script.split(';'):
                command = command.strip()
                if command:  # Check if command is not empty.
                    cursor.execute(command)

        conn.commit()
        print("Database setup completed successfully!")

    except pymysql.MySQLError as err:
        print(f"Error during database setup: {err}")
        if 'conn' in locals() and conn:  # If connection exists, rollback.
            conn.rollback()

    except FileNotFoundError:
        print("SQL file not found at: database/cve_database.sql")

    except Exception as e:  # Catch any other exception.
        print(f"An unexpected error occurred: {e}")
        if 'conn' in locals() and conn:  # If connection exists, rollback.
            conn.rollback()

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    setup_database()