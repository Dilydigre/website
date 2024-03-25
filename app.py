from flask import Flask, render_template, request
import os
import requests as rq
import json

AI_CONTAINER_IP = "172.17.0.2"
if 'AI_CONTAINER_IP' in os.environ:
    AI_CONTAINER_IP = os.environ['AI_CONTAINER_IP'] # retrieve IP of the docker which runs the AI and API
print("AI IP at",AI_CONTAINER_IP)
app = Flask(__name__) 


@app.route('/' method="POST") # La page dont l'url finit par /
def index():
    """Fonction qui s'éxecute lorsque la page est ouverte."""
    return render_template("index.html",visibility="d-none")


@app.route('/explanations', endpoint='explanations') # Page d'explications du fonctionnement de notre modèle "Fonctionnement"
def explanations():
    return render_template("explanations.html")


@app.route('/about', endpoint='about') # Page des licences, les crédits etc... "À Propos"
def explanations():
    return render_template("about.html")


# -- API --
@app.route('/generate',methods = ['GET', 'POST'])
def generate():
    """
    Backend function to call API when user ask to generate an image
    """
    api_result = None
    if request.method == 'GET' or request.data == "": # Only generation without prompt
        r = rq.get("http://"+AI_CONTAINER_IP+":5000/api_v1/generate") # send request to AI/API container
        api_result = json.loads(r.text) # loads returned json
    else:

        data = {'description':request.form.get('description')} # get data passed in post request
        if 'description' in data and 'model' in data: # get prompt of user passed in post data
            if data['model'] == "v1": # if user request to user the first model
                r = rq.post("http://"+AI_CONTAINER_IP+":5000/api_v1/generate_prompt",data=json.dumps({'description': data['description']})) # send post request with user prompt as json data
                api_result = json.loads(r.text)

        elif 'description' in data: # if no model specified, redirect to first version of model
                r = rq.post("http://"+AI_CONTAINER_IP+":5000/api_v1/generate_prompt",data=json.dumps({'description': data['description']})) # send post request with user prompt as json data
                api_result = json.loads(r.text)

    if api_result is not None and api_result['status']:
        return render_template('index.html',b64imagetag=api_result['image'],visibility="") # render base64 encoded image
    return render_template('base.html',visibility="d-none") # if something fails, retur base template