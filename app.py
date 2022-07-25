import joblib
import numpy as np
from flask import Flask, render_template, request
# from sklearn.linear_model import LinearRegression
import os
import pandas as pd
# from sklearn.ensemble import GradientBoostingClassifier
from sklearn import preprocessing
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle

from sklearn.preprocessing import LabelEncoder



app = Flask(__name__, static_folder="templates")

filename = 'finalized_model.sav'
le = LabelEncoder()


filename1 = 'min_max_scalar.sav'
filename2 = 'label_encoder.sav'
scaler = preprocessing.MinMaxScaler()
@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        gender = request.form.get('gender')
        selCity= request.form.get('selCity')
        calorie = request.form.get('eat')
        meals = request.form.get('meals')
        smoke = request.form.get('smoke')
        calories = request.form.get('calories')
        alcohol = request.form.get('alcohol')
        transport = request.form.get('transport')
        MinMaxScalerFile = pickle.load(open(filename1, 'rb'))
        test = MinMaxScalerFile.transform([[height, weight, age]])
        list_2 = [float(x) for item in test for x in item]
        height = list_2[0]
        weight = list_2[1]
        age = list_2[2]
        row = [gender,age,height,weight,selCity, calorie, meals, smoke, calories, alcohol, transport]
        ls = np.array(row, dtype=np.float64)
        load_model = pickle.load(open(filename, 'rb'))
        load_model1 = pickle.load(open(filename2,'rb'))
        result = load_model.predict([ls])
        bmi1 = load_model1.inverse_transform([result][0])
        #bmi1 = le.inverse_transform([(result[0].astype(int))])
        bmi =''.join(str(i) for i in bmi1)

        if((result[0].astype(int)) ==0):
            # 'Insufficient_Weight'
            detail = 'Your BMI is less than 18.5'
            detail2 = 'If the diet is the cause of your low weight, changing to a healthy, balanced diet that provides the right amount of calories for your age, height and how active you are can help you achieve a healthy weight.'
        if((result[0].astype(int)) ==1):
            # 'Normal_Weight'
            detail = 'Your BMI is between 18.5 to 24.9'
            detail2 = 'NICE WORK! Keep your current diet and routine. Emphasize vegetables, fruits, whole grains, and fat-free or low-fat dairy products. Include lean meats, poultry, fish, beans, eggs, and nuts. Limit saturated and trans fats, sodium, and added sugars.'
        if ((result[0].astype(int)) == 2):
            # 'Obesity_Type_I'
            detail = 'Your BMI is between 30 to 34.9'
            detail2 = 'Oopsie. not a good sign. seek GP for more help.'
        if ((result[0].astype(int)) == 3):
            # 'Obesity_Type_II'
            detail = 'Your BMI is between 35 to 39.9'
            detail2 = 'May day May day.. its getting serious here, specialist required to help you out.'
        if ((result[0].astype(int)) == 4):
            # 'Obesity_Type_III'
            detail = 'Your BMI is more than 40'
            detail2 = 'Sign up for gym, go to GP then refer for specialist, hit the PT session, do bootcamp and be strict and follow the diet recommended by dietitian.'
        if ((result[0].astype(int)) == 5):
            # 'Overweight_Level_I'
            detail = 'Your BMI is between 25 to 27.4'
            detail2 = 'Time to go hit the gym and move your sexy ass.'
        if ((result[0].astype(int)) == 6):
            # 'Overweight_Level_II'
            detail = 'Your BMI is between 27.5 to 29.9	'
            detail2 = 'Time to sign up for PT (personal training).'



        return render_template('home.html', scroll='something',  health = bmi,detail = detail, detail2 = detail2)


    
    else:
        return render_template('home.html')
    
 
if __name__ == '__main__':
   app.run(debug = True)


