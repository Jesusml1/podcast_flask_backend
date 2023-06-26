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
`get user's podcasts` [/get-user-podcasts](#get-user-podcasts) <br/>

## POST
`get the episodes of a podcast` [/get-episodes-podcast](#get-episodes-podcast) <br/>
___

### GET /get-user-podcasts
Once user is authenticated you can retrieve data about user podcast

### POST /get-episodes-podcast
Once user is authenticated you can retrieve data about user's podcasts

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `id` | required | string  | podcast id.                                                                     |