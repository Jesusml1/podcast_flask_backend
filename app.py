from flask import Flask, request, render_template, redirect, url_for, flash
import gspread

app = Flask(__name__)

def open_spreadsheet():
    client = gspread.service_account(filename="./secret/credentials.json")
    sheet = client.open("podcast-2023").sheet1
    return sheet

def send_user_new(name, email):
    sheet = open_spreadsheet()
    row = [name, email]
    sheet.append_row(row)

def confirm_user(old_nombre, old_email):
    sheet = open_spreadsheet()
    value1 = sheet.find(old_nombre)
    value2 = sheet.find(old_email)
    row_value1 = value1.row
    row_value2 = value2.row
    if row_value1 == row_value2:
        return row_value1
    else:
        return print("El usuario no existe")

def update_user(new_name, new_email, old_name, old_email):
    sheet = open_spreadsheet()
    row_value = confirm_user(old_name, old_email)
    if row_value:
        sheet.update_cell(row_value, 1, new_name)
        sheet.update_cell(row_value, 2, new_email)
        
    else:
        print("El usuario ya existe")

def delete_user(name, email):
    sheet = open_spreadsheet()
    row_value = confirm_user(name, email)
    if row_value:
        sheet.delete_row(row_value)

@app.route('/')

@app.route('/create_user', methods = ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            print('name is required')
        elif not email:
            print('email is required')
        else:
            send_user_new(name, email)
            return redirect(url_for('get_sheet'))
    return render_template("form_create_user.html")

@app.route('/get_sheet')
def get_sheet():
    sheet = open_spreadsheet()
    data = sheet.get_all_records()
    return str(data)

@app.route('/update_user', methods = ['GET', 'POST'])
def form_update_user():
    if request.method == 'POST':
        old_name = request.form['old_name']
        old_email = request.form['old_email']
        new_name = request.form['new_name']
        new_email = request.form['new_email']

        if not old_name or not old_email:
            print('name or email is required')
        else:
            update_user(new_name, new_email, old_name, old_email)
            return redirect(url_for('get_sheet'))
    return render_template("form_update_user.html")

@app.route('/delete_user', methods = ['GET', 'POST'])
def form_delete_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if not name or not email:
            print('name or email is required')
        else:
            delete_user(name, email)
            return redirect(url_for('get_sheet'))
    return render_template("form_delete_user.html")

if __name__ == '__main__':
    app.run()