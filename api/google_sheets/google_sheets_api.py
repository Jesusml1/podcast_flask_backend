import gspread
from flask import Blueprint, request, jsonify
from settings import settings
import json


google_sheets_bp = Blueprint('google_sheets', __name__)

#funcion para abrir la hoja
def open_spreadsheet():
    client = gspread.service_account_from_dict(settings.CREDENTIALS)
    sheet = client.open("podcast-2023").sheet1
    return sheet

#funcion para comparar si existe un usuario comparando si estan en la misma fila
def confirm_user(old_name, old_email):
    sheet = open_spreadsheet()
    value1 = sheet.find(old_name)
    value2 = sheet.find(old_email)
    row_value1 = value1.row
    row_value2 = value2.row
    if row_value1 == row_value2:
        return row_value1
    else:
        return print("El usuario no existe")

#funcion para crear usuario
def send_user_new(name, email, phone):
    sheet = open_spreadsheet()
    row = [name, email, phone]
    sheet.append_row(row)

#funcion para actualizar usuario
def update_user(new_name, new_email, new_phone , old_name, old_email):
    sheet = open_spreadsheet()
    row_value = confirm_user(old_name, old_email)
    if row_value:
        sheet.update_cell(row_value, 1, new_name)
        sheet.update_cell(row_value, 2, new_email)
        sheet.update_cell(row_value, 3, new_phone)
        
    else:
        print("El usuario ya existe")

#funcion para eliminar usuario
def delete_user(name, email):
    sheet = open_spreadsheet()
    row_value = confirm_user(name, email)
    if row_value:
        sheet.delete_rows(row_value)

#rutas
@google_sheets_bp.route('/create_user', methods = ['POST'])
def create_user():
    if request.method == 'POST':
        name = request.args.get('name')
        email = request.args.get('email')
        phone = request.args.get('phone')
        if name and email and phone:
           send_user_new(name, email, phone)
        else:
            name = request.form['name']
            email = request.form['email']
            if name and email and phone:
               send_user_new(name, email, phone)
            else:
                return jsonify({"message": "error"}), 400
    return jsonify({"message": "Usuario creado", "data": {"new_user": {"name": name, "email": email, "phone": phone}}}), 200

@google_sheets_bp.route('/get_users', methods = ['GET'])
def get_sheet():
    sheet =open_spreadsheet()
    data = sheet.get_all_records()
    return jsonify({"message": "Solicitud exitosa", "data": {"users": data}}), 200

@google_sheets_bp.route('/update_user', methods = ['PUT'])
def form_update_user():
    if request.method == 'PUT':
        old_name = request.args.get('old_name')
        old_email = request.args.get('old_email')
        new_name = request.args.get('new_name')
        new_email = request.args.get('new_email')
        new_phone = request.args.get('new_phone')
        if old_name and old_email and new_phone and new_name and new_email:
           update_user(new_name, new_email, new_phone, old_name, old_email)
        else:
            old_name = request.form['old_name']
            old_email = request.form['old_email']
            new_name = request.form['new_name']
            new_email = request.form['new_email']
            new_phone = request.form['new_phone']
            if old_name and old_email and new_name and new_email:
               update_user(new_name, new_email, new_phone, old_name, old_email)
            else:
                return jsonify({"message": "error"}), 400
    return jsonify({"message": "Usuario actualizado", "data": {"update_user": {"name": new_name, "email": new_email, "phone": new_phone}}}), 200

@google_sheets_bp.route('/delete_user', methods = ['DELETE'])
def form_delete_user():
    if request.method == 'DELETE':
        name = request.args.get('name')
        email = request.args.get('email')
        if name and email:
           delete_user(name, email)
        else:
            name = request.form['name']
            email = request.form['email']
            if name and email:
               delete_user(name, email)
            else:
                return jsonify({"message": "error"}), 400
    return jsonify({"message": "Usuario eliminado"}), 200

#verificar que existe el usuario
def find_user(email):
    sheet = open_spreadsheet()
    cell = sheet.find(email)
    if hasattr(cell, "row"):
        return True
    else:
        return False

#obtener la fila donde esta el registro del usuario    
def get_user_info_row(data):
    sheet = open_spreadsheet()
    cell = sheet.find(data)
    return cell.row

#obtener el id unico del usuario
def get_user_id(email):
    sheet = open_spreadsheet()
    row = get_user_info_row(email)
    id_usuario = sheet.cell(row, 4).value
    return id_usuario

#obtener la informacion del token de spotify del usuario por el id
def get_token_by_user_id(user_id):
    sheet = open_spreadsheet()
    row = get_user_info_row(user_id)
    access_token = sheet.cell(row, 5).value
    expiration_token = sheet.cell(row, 6).value
    refresh_token = sheet.cell(row, 7).value
    return {"access_token": access_token, "expiration_token": expiration_token, "refresh_token": refresh_token}
    
#actualizar la informacion del token del usuario
def insert_spotify_data(data, access_token, token_expiration, refresh_token):
    row_user = get_user_info_row(data)
    sheet = open_spreadsheet()
    sheet.update(f"E{row_user}:G{row_user}", [[access_token, token_expiration, refresh_token]])

#obtener el token del usuario
def get_user_token(user_id):
    return get_token_by_user_id(user_id)
