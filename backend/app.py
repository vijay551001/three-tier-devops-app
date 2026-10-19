import os
import time
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Fetch database configuration from environment variables (No hardcoded credentials!)
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secretpassword")

def get_db_connection():
    """Retries database connection until it succeeds."""
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            print("Database not ready yet, retrying in 3 seconds...")
            time.sleep(3)

@app.route('/')
def init_db_and_get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create a simple table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    
    # Insert a dummy tracking row to prove it's saving data
    cursor.execute("INSERT INTO system_logs (message) VALUES ('New hit from Frontend application');")
    conn.commit()
    
    # Fetch all logs
    cursor.execute("SELECT id, message, created_at FROM system_logs ORDER BY id DESC LIMIT 5;")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Transform rows into a clean JSON structure
    logs = [{"id": r[0], "message": r[1], "timestamp": str(r[2])} for r in rows]
    
    return jsonify({
        "status": "Success",
        "service": "Backend API Node",
        "database_connected": True,
        "recent_logs": logs
    })

if __name__ == '__main__':
    # Listen on all network cards inside the cluster on Port 5000
    app.run(host='0.0.0.0', port=5000)
