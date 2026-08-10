from flask import Flask,render_template,request
import mlflow
import dagshub
import pickle

mlflow.set_tracking_uri('https://dagshub.com/kush10521/mlops-mini-project.mlflow')
dagshub.init(repo_owner='kush10521', repo_name='mlops-mini-project', mlflow=True)

from preprocessing_utility import normalize_text


app=Flask(__name__)

#load the model from model registry
model_name="my_model"
model_version=2

model_uri = f"models:/{model_name}/{model_version}"
model = mlflow.pyfunc.load_model(model_uri)

vectorizer=pickle.load(open('models/vectorizer.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html',result=None)

@app.route('/predict',methods=['POST'])
def predict():
    text=request.form['text']

    #clean
    text=normalize_text(text)

    #Bow
    features=vectorizer.transform([text])

    #predict
    result=model.predict(features)

    #show
    return render_template('index.html',result=result[0])

app.run(debug=True)