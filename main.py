from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/concluido")
def concluido():
    return render_template("concluido.html")        

@app.route("/pendente")
def pendente():
    return render_template("pendente.html")

if __name__ == "__main__":
    app.run()