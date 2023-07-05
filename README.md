# README

### Para crear el entorno virtual
#### windows
`py -3 -m venv .venv`
#### mac/linux
`python3 -m venv .venv`


### Para activar el entorno virtual
#### windows
`.venv\Scripts\activate`
#### mac/linux
`. .venv/bin/activate`

### Para instalar las dependencias 
`pip install -r requirements`

### Para correr servidor local de flask
`flask --app app run`

## 🌐 Desplegado en
https://podcast-flask-backend.onrender.com

# 🛎️ API endpoints

## Spotify


## GET
`solicitar autorización del usuario para obtener información de su cuenta de spotify` [/auth](#auth) <br/>
`obtener los podcast del usuario` [/get-user-podcasts](#get-user-podcasts) <br/>


## POST
`obtener los episodios del podcast del usuario` [/get-episodes-podcast](#get-episodes-podcast) <br/>
___

### GET /auth
Refrescar el access token de spotify

### GET /get-user-podcasts
Devuelve los podcasts del usuario autenticado.

**Parametros**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| ------------
|     `id` | required | string  | user_id.  


### POST /get-episodes-podcast
Devuelve los episodios del podcast solicitado

**Parametros**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| ----------- |
|     `id` | required | string  | user id.          |
|     `podcast_id` | required | string  | access token spotify.
