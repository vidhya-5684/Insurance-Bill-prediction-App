#from pycaret.regression import load_model, predict_model
from sklearn.ensemble import GradientBoostingRegressor
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder




model = pickle.load(open( "fit_model.p", "rb" ))

def transform(data):    
        data['sex'] = pd.factorize(data['sex'])[0]
        data['children'] = pd.factorize(data['children'])[0]
        data['smoker'] = pd.factorize(data['smoker'])[0]
        data['region'] = pd.factorize(data['region'])[0]
        return data

def predict(model, input_df):
    transform_data = transform(input_df)
    predictions_df = model.predict(transform_data)
    predictions = predictions_df[0]
    return predictions_df



#def predict(model, input_df):
    #transform_data = pipeline.fit_transform(input_df)
    #predictions_df = model.predict(transform_data)
   # predictions = predictions_df['Label'][0]
    #
 #return predictions

def run():

    from PIL import Image
   # image = Image.open('logo.png')
    image_hospital = Image.open('hospital.jpg')

   # st.image(image,use_column_width=False)

    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch"))

    st.sidebar.info('This app is created to predict patient hospital charges')
  #  st.sidebar.success('https://www.pycaret.org')
    
    st.sidebar.image(image_hospital)

    st.title("Hospital Charges Prediction App")

    if add_selectbox == 'Online':

        age = st.number_input('Age', min_value=1, max_value=100, value=25)
        sex = st.selectbox('Sex', ['male', 'female'])
        bmi = st.number_input('BMI', min_value=10, max_value=50, value=10)
        children = st.selectbox('Children', [0,1,2,3,4,5,6,7,8,9,10])
        if st.checkbox('Smoker'):
            smoker = 'yes'
        else:
            smoker = 'no'
        region = st.selectbox('Region', ['southwest', 'northwest', 'northeast', 'southeast'])

        output=""

        input_dict = {'age' : age, 'sex' : sex, 'bmi' : bmi, 'children' : children, 'smoker' : smoker, 'region' : region}
        print(input_dict)
        input_df = pd.DataFrame([input_dict])
        print(input_df)

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            output = '$' + str(np.round(output[0],4))

        st.success('The bill is {}'.format(output))
       

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload,sep=',')                       
            predictions = predict(model,data) 
            predictions = pd.DataFrame(predictions,columns = ['Charges($)'])
         #   predictions.columns = ['Bill']
            st.write(predictions)

if __name__ == '__main__':
    run()
