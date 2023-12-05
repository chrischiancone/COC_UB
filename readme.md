Importing Necessary Libraries and Initializing Flask App

Flask is imported from the flask package to create the web application.
request is used to handle HTTP requests.
render_template_string allows rendering an HTML template from a string directly.
flash and redirect are for displaying messages and redirecting the user.
csv is used for reading from and writing to CSV files.
socket is imported but not used in the script.
The Flask app is created with app = Flask(__name__).
A secret key for the Flask application is set, important for session management and security.
Function: Get User's IP Address

get_ip_address(request): Retrieves the IP address of the user making the request. If there is an "X-Forwarded-For" header (common in proxied environments), it uses that; otherwise, it falls back to request.remote_addr.
Function: Find New Account Number

find_new_account_number(legacy_account_number, csv_path): Opens a CSV file and searches for a row where the 'hteAcctNum' field matches the provided legacy account number. If found, it returns the corresponding 'vx1ActNum' (presumably the new account number).
Function: Append Data to CSV

append_to_csv(data, output_csv_path): Appends a row of data to the specified CSV file.
Flask Route for the Home Page

@app.route('/', methods=['GET', 'POST']): A route to handle both GET and POST requests to the home page URL ('/').
If the request is POST (form submission), it processes the submitted legacy account number, looks up the new account number, and records the activity with IP address in another CSV file.
If the new account number is found, it flashes a success message; otherwise, it flashes an error message.
The function returns rendered HTML for the page, which includes a form for inputting the legacy account number.
HTML Template Embedded in Python Script

The HTML template for the web page is embedded directly within the Python script using render_template_string. This HTML includes a form where users can input their legacy account number.
The template uses Bootstrap styling for elements like forms and messages.
Running the Flask App

The if __name__ == '__main__': line checks if the script is being run directly (not imported as a module).
app.run(debug=True, host='0.0.0.0'): Runs the Flask app with debugging enabled and makes the server externally visible.