# Se debe ejecutar con la terminal cmd (Command Prompt)
# Para crear un entorno virtual en python con el nombre de env
# python -m venv env

# Para activar el entorno virtual, se verifica con (env)
# call env/scripts/activate

# Para instalar las librerias que estan en requirements
# pip install -r requirements.txt

# Para correr el servidor flask
# flask --app app.py --debug run

# Importar librerias
from flask import Flask, request, jsonify
from pulp import *

# Configuracion proyecto
app = Flask(__name__)

@app.route("/")
def hello_world():
    json_file = {}
    json_file['query'] = 'Hello World, Api Calcula Cortes'
    return jsonify(json_file)

if __name__ == "__main__":
    app.run(port=56290)


# Metodos de llamada
# Se ejecuta cuando visito la url http://127.0.0.1:5000/calcularOptimo/2/3/11/10
@app.route("/calcularOptimo/<float:anchoCorte>/<float:largoCorte>/<float:anchoPliego>/<float:largoPliego>")
def calcularOptimo(anchoCorte,largoCorte,anchoPliego,largoPliego):
    problema = LpProblem("Problema_Optimizacion_lineal",LpMaximize)
    x = LpVariable("X", lowBound=0, cat="Integer")
    y = LpVariable("Y", lowBound=0, cat="Integer")

    ## Funcion Objetivo
    problema += x+y

    ## Restricciones
    problema += anchoCorte*x+largoCorte*y<=anchoPliego
    problema += largoCorte*x+anchoCorte*y<=largoPliego

    problema.solve()
    solucion = {"X": int(x.varValue), 
                "Y": int(y.varValue)}
    
    return jsonify(solucion), 200