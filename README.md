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

## Desplegado en
https://podcast-flask-backend.onrender.com

# API endpoints

## Spotify


## GET
`obtener los podcast del usuario` [/get-user-podcasts](#get-user-podcasts) <br/>

## POST
`obtener los episodios del podcast del usuario` [/get-episodes-podcast](#get-episodes-podcast) <br/>
`refrescar el access token` [/refresh](#refresh) <br/>
___

### GET /get-user-podcasts
Devuelve los podcasts del usuario autenticado.

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `token` | required | string  | access token spotify.  
--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `token_expiration` | required | string  | expiration token.  

### POST /get-episodes-podcast
Devuelve los episodios del podcast solicitado

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `podcast_id` | required | string  | podcast id.                                                                                                                         |
--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `token` | required | string  | access token spotify.  
--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `token_expiration` | required | string  | token expiration. 

### POST /refresh
Refrescar el access tokoen de spotify
**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `podcast_id` | required | string  | podcast id.                                                                                                                         |
--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `token` | required | string  | access token spotify.  
--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `token_expiration` | required | string  | token expiration. 