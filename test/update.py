#!/usr/bin/env python
import pygsheets
import sys
import csv
#import openpyxl
#import gspread
#print(openpyxl.__version__)

user_choice = {"y": True, "n": False}

def read_csv(in_filename):

    with open(in_filename) as file:
        reader = csv.reader(file, delimiter=',', quotechar='|')

        rows = []
        for row in reader:
            rows.append(row)
        return rows


def yn_prompt(prompt):
    while True:
        sys.stdout.write(prompt)
        choice = input().lower()
        if choice in user_choice:
            break
        else:
            sys.stdout.write("Respond with 'yes' or 'no' "
                                "(or 'y' or 'n').\n")
    return choice


def new_sheet(choice):
    if user_choice[choice]:
        while True:
            sys.stdout.write("Name of Google Sheet: ")
            choice = input().lower()
            if choice != "":
                break
            else:
                sys.stdout.write(
                    "Provide a name for the Google Sheet.\n")
        return choice
    else:
        return None


def main(in_filename, out_filename):

    gc = pygsheets.authorize(
        outh_file="client_secret.json",
        outh_nonlocal=True)

    all_sheets = gc.list_ssheets()
    all_names = [sheet['name'] for sheet in all_sheets]

    sheet_name = None
    if out_filename is None:
        choice = yn_prompt("Would you like to create a new sheet? [y/n] ")
        sheet_name = new_sheet(choice)

    if sheet_name is not None:
        gc.create(sheet_name)
    elif out_filename is not None and sheet_name is None:
        sheet_name = out_filename
    else:
        while True:
            sys.stdout.write("Name of Google Sheet: ")
            sheet_name = input().lower()
            if sheet_name != "" and sheet_name in all_names:
                break
            elif sheet_name not in all_names:
                choice = yn_prompt(
                    "Sheet does not exist. Would you like to create a new sheet? [y/n] ")
                if user_choice[choice]:
                    sheet_name = new_sheet(choice)
                    gc.create(sheet_name)
                    break
            else:
                sys.stdout.write(
                    "Please respond with the name of the Google Sheet.\n")
    #wksheet_choice = #sheet_choice
    sh = gc.open(sheet_name)
#    if sheet_choice == '1':
#        wks = sh.get_worksheet(1)
#    else:
    wks = sh.sheet1
    # gc.open(sheet_name).get_worksheet(1)
#    elif sheet_choice == "sheet2":
#        wks = sh.sheet2
#    elif sheet_choice == "sheet3":
#        wks = sh.sheet3
#    else:
#        print "sheetname not found"


    read_from_file = read_csv(in_filename)
    for row in read_from_file:
        rows = len(wks.get_col(2, returnas='cell', include_empty=False))
        wks.append_table(start=("A" + str(rows + 1)), end=None, values=row)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Error: Wrong number of arguments\nUsage: python auth.py <CSV filename> <Google spreadsheet name>")
    elif len(sys.argv) == 2:
        # Input file: filename.csv, Output file: gsheet name
        main(sys.argv[1], None)
    else:
        # Input file: filename.csv, Output file: gsheet name
        main(sys.argv[1], sys.argv[2])
