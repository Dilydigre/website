from flask import Flask, render_template

app = Flask(__name__) 


@app.route('/') # La page dont l'url finit par /
def index():
    """Fonction qui s'éxecute lorsque la page est ouverte."""
    return render_template("index.html")