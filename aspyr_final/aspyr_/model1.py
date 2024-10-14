import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import render_template, Flask, request, jsonify
from flask_cors import CORS

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('aspyr(gs1)')

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    principal = float(data.get('principal'))
    rate = float(data.get('rate'))
    time = int(data.get('time'))

    # Write values to the Google Sheet (Input sheet)
    input_sheet = sheet.worksheet('input')
    input_sheet.update('B2', [[principal]])
    input_sheet.update('B3', [[rate]])
    input_sheet.update('B4', [[time]])

    # Read the calculated Simple Interest result from the Output sheet (A1)
    output_sheet = sheet.worksheet('output')
    simple_interest = output_sheet.acell('A1').value

    # Read the calculated Compound Interest result from the Output sheet (A2)
    compound_interest = output_sheet.acell('A2').value

    # Return both the simple and compound interest as JSON
    return jsonify({
        "simple_interest": simple_interest,
        "compound_interest": compound_interest
    })

if __name__ == '__main__':
    app.run(debug=True)
