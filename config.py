import os

# Load database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "default_user")  # Provide a default user if not set
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")
DB_NAME = os.getenv("DB_NAME", "default_db")

# Load API configuration from environment variables
API_URL = os.getenv("API_URL", "https://services.nvd.nist.gov/rest/json/cves/2.0")
RESULTS_PER_PAGE = int(os.getenv("RESULTS_PER_PAGE", 2000))  # Convert to integer
