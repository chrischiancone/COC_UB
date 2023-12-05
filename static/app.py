from flask import Flask, request, render_template_string, flash, redirect
from markupsafe import Markup
import csv

app = Flask(__name__)
# Replace 'supersecretkey' with a real secret key for production
app.secret_key = 'supersecretkey'

# Function to get the user's IP address
def get_ip_address():
    if request.headers.getlist("X-Forwarded-For"):
        ip_address = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_address = request.remote_addr
    return ip_address

# Function to search for the new account number in the CSV file
def find_new_account_number(legacy_account_number, csv_path):
    with open(csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['hteAcctNum'] == legacy_account_number:
                return row['vx1ActNum']
    return None

# Function to append data to a CSV file
def append_to_csv(data, output_csv_path):
    with open(output_csv_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

# Flask route for the home page with the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        legacy_account_number = request.form.get('legacy_account_number')
        csv_path = 'CAR Cross Reference.csv'  # Ensure this path is correct
        output_csv_path = 'output_data.csv'  # Ensure this path is correct
        new_account_number = find_new_account_number(legacy_account_number, csv_path)

        if new_account_number:
            ip_address = get_ip_address()
            append_to_csv([legacy_account_number, new_account_number, ip_address], output_csv_path)
            # Use Markup to safely render HTML content
            message = Markup(f'Your new account number is: <a href="https://myaccount.cityofcarrollton.com/register?account={new_account_number}">{new_account_number}</a>')
            flash(message)
            return redirect('/')
        else:
            flash('Invalid account number. Please try again.')
            return redirect('/')

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<script>
    function copyToClipboard(elementId) {
    var copyText = document.getElementById(elementId);
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices
    document.execCommand("copy");
    alert("Copied the text: " + copyText.value); // Optional: alert the copied text
        }
</script>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Number Lookup</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 20px;
        }
        label {
            font-weight: bold;
        }
        input[type=text] {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        input[type=submit] {
            padding: 10px 20px;
            background-color: #2f5d7a;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type=submit]:hover {
            background-color: #4cae4c;
        }
        .logo {
            display: block;
            margin: 0 auto 20px auto;
            max-width: 200px; /* Adjust as per your logo's dimensions */
        }
        .messages {
            color: #d9534f;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="container">
        <img src="{{ url_for('static', filename='logo.png') }}" alt="City of Carrollton" class="logo">
        <h1>Account Number Lookup</h1>
        {% with messages = get_flashed_messages(with_categories=false) %}
          {% if messages %}
            <div class="messages">
            {% for message in messages %}
              <p>{{ message }}</p>
            {% endfor %}
            </div>
          {% endif %}
        {% endwith %}
        <form action="/" method="post">
            <label for="legacy_account_number">Enter your current account number:</label>
            <input type="text" id="legacy_account_number" name="legacy_account_number" required>
            <input type="submit" value="Lookup">
        </form>
    </div>
</body>
</html>

""")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
