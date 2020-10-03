from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict(): 
    try:
        # Recuperamos los datos del formulario web
        valores=request.form.to_dict()
        df_input= pd.DataFrame([valores])
        # Cargamos el dataset con los juegos
        juegos=pd.read_csv('juegos.csv')
        juegos.dropna(axis=0,inplace=True)
        
        # ponemos todo en Mayusculas
        juegos['juego-upper']=juegos['juego'].str.upper()
        df_input['src-juego-upper']=df_input['src-juego'].str.upper()
        
        juegos_query=juegos[ (juegos['juego-upper'].str.find( df_input['src-juego-upper'].iloc[0] )!=-1) ]
        #juegos_query=juegos[ (juegos['juego'].str.find( 'ario' )!=-1) ]
        juegos_query=juegos_query[['tienda','juego','precio','fecha']].sort_values(by=['tienda','precio'], ascending=False)
        
        return render_template("index.html", Resultado=[juegos_query.to_html(classes='renfe', header="true")])
    
    except:
        return render_template("index.html", Error="RUTA NO ENCONTRADA"+str(valores))
        

if __name__=="__main__":
    app.run(host='0.0.0.0')




