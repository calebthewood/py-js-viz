# import json
import gspread
import pandas

MICROBE_URL = 'https://docs.google.com/spreadsheets/d/1kHCEWY-d9HXlWrft9jjRQ2xf6WHQlmwyrXel6wjxkW8/edit#gid=0'
gc = gspread.service_account(filename='./config/service_account.json')

sh = gc.open("Microbe-scope") # can open by name, id, or url

sh.worksheets() # view worksheets

ws = sh.worksheet('bugs') # get a single worksheet
ws.col_values(2) # 1 gets column A, B is 2, etc...

# expected_headers=[], empty headers cause get_all_records to fail and this
# spreadsheet has headers & subheaders with many blanks. Can either pass
# an empty array to get everything, or pass an array of col titles to get
df = pandas.DataFrame(ws.get_all_records(expected_headers=[]))
df.info()