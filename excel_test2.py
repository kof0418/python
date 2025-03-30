from openpyxl import Workbook
import csv

data_rows = [fields for fields in csv.reader(open("file.csv", newline=""))]

wb = Workbook()
ws = wb.active
ws.title = "MyFile"
ws.sheet_properties.tabColor = "1072BA"
for row in data_rows:
    ws.append(row)

wb.save("Myfile.xlsx")
