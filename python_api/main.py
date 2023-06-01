from flask import Flask, jsonify, request
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
import time

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="db",
    database="mydb",
    user="myuser",
    password="mypassword"
)

app = Flask(__name__)
# Create a histogram to track the response time of requests
REQUEST_TIME = Histogram('request_processing_seconds', 'Time spent processing request')

# Instrument the / endpoint with the REQUEST_TIME histogram
@app.route('/')
@REQUEST_TIME.time()
def hello_world():
        return 'Hello, World!'

# Instrument the /ping endpoint with the REQUEST_TIME histogram
@app.route('/ping')
@REQUEST_TIME.time()
def ping():
    time.sleep(2)  # Simulate some processing time
    return 'pong'

# Define the endpoint to expose the Prometheus metrics
@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/users', methods=['GET'])
@REQUEST_TIME.time()
def get_users():
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users")
    rows = cur.fetchall()
    users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in rows]
    cur.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
@REQUEST_TIME.time()
def add_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({'id': id, 'name': name, 'email': email})

if __name__ == '__main__':
    # Start the server
    app.run(debug=True, host='0.0.0.0', port=8888)

