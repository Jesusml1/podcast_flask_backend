
from flask import Flask, request, url_for, session, redirect, make_response, jsonify, render_template, flash
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import gspread
import api.spotify.spotify as spotifyAPI

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

# --- spotify

#endpoint para autenticar al usuario y pedir autorizacion
@app.route("/auth")
def auth():
    auth_url = spotifyAPI.auth()

    return redirect(auth_url)

#solicita y guarda el token en la sesion y redirige al dashboard
@app.route("/redirect")
def redirect_page():
   
    code = request.args.get('code')
    spotifyAPI.request_token(code)

    return redirect(url_for('dashboard', _external = True))
    
#obtener todos los podcast de un usuario
@app.route("/get-user-podcasts")
def  get_user_podcasts():
    response = spotifyAPI.get_user_podcasts()

    return response

#obtener los episodios de un podcast
@app.route("/get-episodes-podcast", methods=['POST'])
def  get_episodes():
        
    data = request.get_json()
    podcast_id  = data.get('id')
    response = spotifyAPI.get_episodes_podcast(podcast_id)

    return response

@app.route("/")
def dashboard():
    return "<p>Dashboard</p>"

@app.route('/logout')
def logout():
    session.clear()
    return ('sesión finalizada')

# --- google sheets

#funcion para abrir la hoja
def open_spreadsheet():
    client = gspread.service_account(filename="./secret/credentials.json")
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
@app.route('/create_user', methods = ['POST'])
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

@app.route('/get_users', methods = ['GET'])
def get_sheet():
    sheet = open_spreadsheet()
    data = sheet.get_all_records()
    return jsonify({"message": "Solicitud exitosa", "data": {"users": data}}), 200

@app.route('/update_user', methods = ['PUT'])
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

@app.route('/delete_user', methods = ['DELETE'])
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



