import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, render_template

# I have the JSON set up but you need to point it correctly, adjust for your system.
CREDENTIALS_FILE = 'C:/path/to/JSON/Fix/On/Your/Implementation/client_secret_223834847755-k95bp17fol3k51iqjapvpc8ujh7o8o7q.apps.googleusercontent.com.json'

app = Flask(__name__)

def authenticate_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def compile_data_from_spreadsheets(client, spreadsheet_ids):
    data = []
    for spreadsheet_id in spreadsheet_ids:
        try:
            sheet = client.open_by_key(spreadsheet_id)
            worksheet = sheet.get_worksheet(0)  # Assuming the data is on the first worksheet, change if needed
            rows = worksheet.get_all_values()
            data.extend(rows[1:])  # Skip the header row
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Spreadsheet with ID '{spreadsheet_id}' not found.")
        except Exception as e:
            print(f"Error retrieving data from spreadsheet with ID '{spreadsheet_id}': {e}")
    return data

def filter_by_availability(data, available_only):
    if available_only:
        data = [row for row in data if row[0].lower() == 'y']
    return data

def filter_by_category(data, category):
    if category:
        category_index = data[0].index('category')
        data = [row for row in data if row[category_index].lower() == category.lower()]
    return data

#This is whatever the opposite of graceful is, come back and clean
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        available_only = 'available_only' in request.form
        category = request.form['category']

        client = authenticate_google_sheets()
        data = compile_data_from_spreadsheets(client, SPREADSHEET_IDS)

        if search_term:
            data = [row for row in data if any(search_term.lower() in cell.lower() for cell in row)]

        data = filter_by_availability(data, available_only)
        data = filter_by_category(data, category)

        dropdown_html = "<select>"
        for row in data:
            dropdown_html += "<option>" + " | ".join(row) + "</option>"
        dropdown_html += "</select>"
        return render_template('index.html', dropdown_html=dropdown_html)

    return render_template('index.html')

if __name__ == "__main__":
    # Replace these with the just the last numbers in your spreadsheets
    SPREADSHEET_IDS = ['spreadsheet_id_1', 'spreadsheet_id_2', 'spreadsheet_id_3']

    app.run(debug=True)
    
if __name__ == "__debug"
    #

