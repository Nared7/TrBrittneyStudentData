# import pandas as pd
import pandas as pd
import streamlit as st
import gspread
import json

# import matplotlib.pyplot as plt
from string import capwords


Name = st.text_input('Which student are you looking for?')

cred_file = r"trbrittneystudentdata-bb3d38df148f.json"
gc = gspread.service_account(filename=cred_file)
database = gc.open('studentData')
invoiceData = gc.open('InvoiceList_March2023')

st.info('Data is loaded from local Database')
st.info('Click "Fetch Data" to update the Database')
with open('studentData.json') as json_file:
    allStData = json.load(json_file)

with open('invoiceData.json') as json_file:
    invoice_data = json.load(json_file)


db_studentName = []
db_engClassPrice = []
db_engClassDiscount = []
db_engClassNetPrice = []
db_grammarClassPrice = []
db_grammarClassDiscount = []
db_grammarClassNetPrice = []
db_bookPrice = []
db_totalCost = []
db_totalCost_withoutBookFee = []
db_studentClass = []
tag = []
stData = []

in_amount = []
in_class = []
in_id = []
in_note = []
in_stName = []
in_TranID = []
stInvoiceData = []


def fetchData():
    global allStData, invoice_data
    ws_list = database.worksheets()
    invoice_ws = invoiceData.worksheets()

    for sheet in ws_list:
        list_of_dicts = sheet.get_all_records()

        #       Remove whitespace the data
        for i in range(len(list_of_dicts)):
            list_of_dicts[i] = {x.strip(): v for x, v in list_of_dicts[i].items()}

        allStData[sheet.title] = list_of_dicts

    for sheet in invoice_ws:
        list_of_dicts = sheet.get_all_records()

        #       Remove whitespace the data
        for i in range(len(list_of_dicts)):
            list_of_dicts[i] = {x.strip(): v for x, v in list_of_dicts[i].items()}

        invoice_data[sheet.title] = list_of_dicts


    with open("studentData.json", "w") as write_file:
        json.dump(allStData, write_file, indent=4, separators=(", ", ": "), sort_keys=True)  # encode dict into JSON

    with open("invoiceData.json", "w") as write_file:
        json.dump(invoice_data, write_file, indent=4, separators=(", ", ": "), sort_keys=True)  # encode dict into JSON



def searchName(name):
    global allStData, stData

    db_studentName.clear()
    db_engClassPrice.clear()
    db_engClassDiscount.clear()
    db_engClassNetPrice.clear()
    db_grammarClassPrice.clear()
    db_grammarClassDiscount.clear()
    db_grammarClassNetPrice.clear()
    db_bookPrice.clear()
    db_totalCost.clear()
    db_totalCost_withoutBookFee.clear()
    db_studentClass.clear()

    in_amount.clear()
    in_class.clear()
    in_id.clear()
    in_note.clear()
    in_stName.clear()
    in_TranID.clear()

    inputStName = name

    for database_className, database_students in allStData.items():
        for database_singleStudent in database_students:
            # print(database_singleStudent['Myanmar Name'])
            if inputStName.lower() in database_singleStudent['Myanmar Name'].lower():
                print(database_singleStudent['Myanmar Name'])
                db_studentName.append(database_singleStudent['Myanmar Name'])
                db_engClassPrice.append(database_singleStudent['4 Skill Class Fee (Monthly)'])
                db_engClassDiscount.append(database_singleStudent['4Skill Discount (%)'])
                db_engClassNetPrice.append(database_singleStudent['Net Fee (4 Skill)'])

                try:
                    db_grammarClassPrice.append(database_singleStudent['Grammar Class Fee (Monthly)'])
                    db_grammarClassDiscount.append(database_singleStudent['Grammar Discount (%)'])
                    db_grammarClassNetPrice.append(database_singleStudent['Net Fee (Grammar)'])
                except:
                    db_grammarClassPrice.append('    -    ')
                    db_grammarClassDiscount.append('    -    ')
                    db_grammarClassNetPrice.append('    -    ')

                db_bookPrice.append(database_singleStudent['Book Fee (One School Year)'])
                db_totalCost.append(database_singleStudent['Total Cost'])
                db_totalCost_withoutBookFee.append(database_singleStudent['Total Cost (Without Book Fee)'])
                db_studentClass.append(database_className)

    for database_className, database_students in invoice_data.items():
        for database_singleStudent in database_students:
            # print(database_singleStudent['Myanmar Name'])
            if inputStName.lower() in database_singleStudent['Student Name'].lower():
                # print(database_singleStudent['Student Name'])
                in_stName.append(database_singleStudent['Student Name'])
                in_id.append(database_singleStudent['Invoice ID'])
                in_TranID.append(database_singleStudent['Transaction ID'])
                in_amount.append(database_singleStudent['Amount'])
                in_class.append(database_className)
                in_note.append(database_singleStudent['Note'])

    for i in range(len(db_studentName)):
        stData.append(
            [db_studentName[i], db_studentClass[i], db_engClassPrice[i], db_engClassDiscount[i],
             db_engClassNetPrice[i],
             db_grammarClassPrice[i], db_grammarClassDiscount[i], db_grammarClassNetPrice[i],
             db_bookPrice[i], db_totalCost[i],
             db_totalCost_withoutBookFee[i]]) # tuple = python data type, list & dictionary = python data type

    for i in range(len(in_stName)):
        stInvoiceData.append(
            [in_stName[i], in_class[i], in_id[i], in_TranID[i], in_amount[i], in_note[i]]) # tuple = python data type, list & dictionary = python data type


st.button('Fetch Data', on_click=fetchData)
searchName(Name)

stLabel = ['Name', 'Class', '4 Skill Class Fee', '4 Skill Discount', '4 Skill Net Fee', 'Grammar Class Fee', 'Grammar Discount', 'Grammar Net Fee', 'Book Fee', 'Total Cost', 'Total Cost(Without Book Fee']
stInvoiceLabel = ['Name', 'Class', 'Invoice ID', 'Kpay ID', 'Amount', 'Note']
pdDataFrame = pd.DataFrame(stData, columns=stLabel)
pdInvoiceDataFrame = pd.DataFrame(stInvoiceData, columns=stInvoiceLabel)
st.table(pdDataFrame)
st.table(pdInvoiceDataFrame)

