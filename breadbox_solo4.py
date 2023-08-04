import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Change this so it points to the JSON in question on your system
CREDENTIALS_FILE = 'path/to/JSON/client_secret_223834847755-k95bp17fol3k51iqjapvpc8ujh7o8o7q.apps.googleusercontent.com.json'

def authenticate_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def retrieve_data_from_spreadsheets(client, spreadsheet_ids):
    data = {}
    for spreadsheet_id in spreadsheet_ids:
        try:
            sheet = client.open_by_key(spreadsheet_id)
            worksheet = sheet.get_worksheet(0)  # Assuming the data is on the first worksheet, change if needed
            data[spreadsheet_id] = worksheet.get_all_values()
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Spreadsheet with ID '{spreadsheet_id}' not found.")
        except Exception as e:
            print(f"Error retrieving data from spreadsheet with ID '{spreadsheet_id}': {e}")
    return data

def filter_rows_by_term(data, search_term):
    filtered_rows = []
    for spreadsheet_id, rows in data.items():
        for row in rows[1:]:  # Skip the header row
            if search_term.lower() in [cell.lower() for cell in row]:
                filtered_rows.append(row)
    return filtered_rows

if __name__ == "__main__":
    # This system needs JUST the Spreadsheet ID, just the numbers at the end of the URL
    SPREADSHEET_IDS = ['spreadsheet_id_1', 'spreadsheet_id_2', 'spreadsheet_id_3']

    # Authenticaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaate
    gs_client = authenticate_google_sheets()

    # This is functional for now but would be one of my first areas to expand
    data_from_spreadsheets = retrieve_data_from_spreadsheets(gs_client, SPREADSHEET_IDS)

    # This is coded as an input for testing, change this for final implementation
    search_term = input("Enter the test term:")

    # Filtering for the searched term is a simple command
    filtered_rows = filter_rows_by_term(data_from_spreadsheets, search_term)

    # This works for a pretty simple addition but there's better ways to do this I think
    dropdown_html = "<select>"
    for row in filtered_rows:
        dropdown_html += "<option>" + " | ".join(row) + "</option>"
    dropdown_html += "</select>"

    print(dropdown_html)

