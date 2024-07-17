from flask import Flask, request, send_file
import logging
import sqlite3
import subprocess
import requests
import xml.etree.ElementTree as ET
import os
import base64

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def validate_user(username, password):
    validation_endpoint = "http://example.com/validate"  # Replace with the actual endpoint
    
    # Base64 encode the password
    encoded_password = base64.b64encode(password.encode()).decode()
    
    response = requests.post(validation_endpoint, data={'username': username, 'password': encoded_password})
    if response.status_code == 200:
        return response.json().get('valid', False)
    return False

@app.route('/dashboard', methods=['POST'])
def create_dashboard():
    try:
        # Get username and password from request
        username = request.form['username']
        password = request.form['password']
        
        # Log username and password (insecure)
        logging.info(f'Username: {username}, Password: {password}')
        
        # Validate the username and password with an external entity
        if not validate_user(username, password):
            return "Invalid username or password", 403

        # Get user input for SQL query (insecure)
        user_input = request.form['user_input']
        
        # Run insecure SQL query
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM data WHERE column = '{user_input}'")
        data = cursor.fetchall()
        conn.close()

        # XML entity expansion (insecure)
        xml_data = request.form['xml_data']
        try:
            root = ET.fromstring(xml_data)
            logging.info(f'Parsed XML: {ET.tostring(root, encoding="unicode")}')
        except ET.ParseError as e:
            # Improper error handling: Disclose internal details
            logging.error(f'Error parsing XML: {e}')
            return f"XML Parse Error: {e}", 400
        
        # Use username in subprocess query to create a new dashboard (insecure)
        dashboard_file = f"{username}_dashboard.txt"
        subprocess.run(f'touch {dashboard_file}', shell=True)  # Vulnerable to command injection

        # Set file permissions to be overly permissive (rwxrwxrwx)
        os.chmod(dashboard_file, 0o777)
        
        # Return the dashboard file as a downloadable file
        return send_file(dashboard_file, as_attachment=True)

    except Exception as e:
        # Improper error handling: Return generic error message
        logging.error(f'An unexpected error occurred: {e}')
        return "An unexpected error occurred. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
