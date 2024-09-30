import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

import sklearn
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import xgboost as xgb
import lightgbm as lgb

import joblib

from utils import *

data_columns = ['DM (kg/d)', 'OM (kg/d)', 'CP (kg/d)', 'NDF (kg/d)', 'Lipid (kg/d)', 'Bacteria: prevotellaceae ucg-001', 'Bacteria: prevotellaceae ga6a1 group', 'Bacteria: rikenellaceae rc9 gut group', 'Bacteria: u29-b03', 'Bacteria: lachnospiraceae nk3a20 group', 'Bacteria: anaerosporobacter', 'Bacteria: marvinbryantia', 'Bacteria: oribacterium', 'Bacteria: lachnospiraceae ucg-001', 'Bacteria: cag-352', 'Bacteria: uncultured.2', 'Bacteria: saccharofermentans', 'Bacteria: anaeroplasma', 'Bacteria: ned5e9', 'Bacteria: veillonellaceae ucg-001', 'Bacteria: succinivibrionaceae ucg-001', 'Bacteria: succinivibrionaceae ucg-002', 'Bacteria: ruminobacter', 'Bacteria: succinimonas', 'Bacteria: uncultured.8', 'Bacteria: acetobacter', 'Bacteria: olsenella', 'Bacteria: desulfovibrio', 'Bacteria: cpla-4 termite group', 'Bacteria: endomicrobium', 'Archaea: methanosphaera', 'Archaea: candidatus methanomethylophilus', 'Archaea: uncultured', 'Protozoa: ophryoscolex', 'Protozoa: polyplastron',
       'Protozoa: dasytricha', 'Protozoa: diplodinium', 'Protozoa: diploplastron', 'Protozoa: entodinium', 'Fungi: neocallimastix', 'Fungi: piromyces', 'Fungi: caecomyces', 'Fungi: aklioshbomyces', 'Herd IT1', 'Herd IT2', 'Herd IT3', 'Herd UK1', 'Herd UK2']

methane_data = pd.read_csv('wallace_metadata.csv')
methane_label = methane_data.iloc[:, -1]
methane_data = methane_data.iloc[:, 1:-1]
herd_data = methane_data.iloc[:,5:10]

herd_model = joblib.load('knn_model_herd.pkl')
lightgbm_model = joblib.load('lightgbm_model.pkl')
xgboost_model = joblib.load('xgb_model.pkl')
svr_model = joblib.load('svr_model.pkl')
elastic_model = joblib.load('elastic_model.pkl')
knn_model = joblib.load('knn_model.pkl') 
mlp_model = MethaneModel(len(data_columns))
mlp_model.load_state_dict(torch.load('methane_model.pth'))

mlp_model.eval()

# Define the data columns
DATA_COLUMNS = ['DM (kg/d)', 'OM (kg/d)', 'CP (kg/d)', 'NDF (kg/d)', 'Lipid (kg/d)', 
                'Bacteria: prevotellaceae ucg-001', 'Bacteria: prevotellaceae ga6a1 group', 
                'Bacteria: rikenellaceae rc9 gut group', 'Bacteria: u29-b03', 
                'Bacteria: lachnospiraceae nk3a20 group', 'Bacteria: anaerosporobacter', 
                'Bacteria: marvinbryantia', 'Bacteria: oribacterium', 'Bacteria: lachnospiraceae ucg-001', 
                'Bacteria: cag-352', 'Bacteria: uncultured.2', 'Bacteria: saccharofermentans', 
                'Bacteria: anaeroplasma', 'Bacteria: ned5e9', 'Bacteria: veillonellaceae ucg-001', 
                'Bacteria: succinivibrionaceae ucg-001', 'Bacteria: succinivibrionaceae ucg-002', 
                'Bacteria: ruminobacter', 'Bacteria: succinimonas', 'Bacteria: uncultured.8', 
                'Bacteria: acetobacter', 'Bacteria: olsenella', 'Bacteria: desulfovibrio', 
                'Bacteria: cpla-4 termite group', 'Bacteria: endomicrobium', 'Archaea: methanosphaera', 
                'Archaea: candidatus methanomethylophilus', 'Archaea: uncultured', 'Protozoa: ophryoscolex', 
                'Protozoa: polyplastron', 'Protozoa: dasytricha', 'Protozoa: diplodinium', 
                'Protozoa: diploplastron', 'Protozoa: entodinium', 'Fungi: neocallimastix', 
                'Fungi: piromyces', 'Fungi: caecomyces', 'Fungi: aklioshbomyces', 
                'Herd IT1', 'Herd IT2', 'Herd IT3', 'Herd UK1', 'Herd UK2']

methane_data = methane_data[DATA_COLUMNS]

preprocess = StandardScaler()
preprocess.fit(methane_data)

st.title('Methane Emission Prediction for Cattle 🐮')
st.header('Input Cattle Feed Information') 
with st.expander("Enter numbers", expanded=True):
    dm = st.number_input('DM (kg/d)', min_value=0.0, max_value=100.0, value=20.0, step=0.1)
    om = st.number_input('OM (kg/d)', min_value=0.0, max_value=100.0, value=15.0, step=0.1)
    cp = st.number_input('CP (kg/d)', min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    ndf = st.number_input('NDF (kg/d)', min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    lipid = st.number_input('Lipid (kg/d)', min_value=0.0, max_value=100.0, value=2.0, step=0.1)

# st.header('Predicted Herd')
feed_data = np.array([[dm, om, cp, ndf, lipid]])
predicted_herd = herd_model.predict(feed_data)
# st.write(f'This cow belongs to Herd {predicted_herd[0]}')

model_option = st.selectbox('Choose a model for prediction', 
                            ('MLP', 'LightGBM', 'XGBoost', 'SVR', 'Elastic Net', 'KNN'))

st.header('Input Microbiome Data')
microbiome_data = []
with st.expander("Enter numbers", expanded=False):
    for feature in DATA_COLUMNS[5:-5]:
        value = st.slider(f'{feature}', min_value=-1.0, max_value=5.0, value=0.0, step=0.01)
        microbiome_data.append(value)
    microbiome_data = np.array(microbiome_data)

herd = np.zeros(5) 
if predicted_herd[0] == 1:
    herd[0] = 1
elif predicted_herd[0] == 2:
    herd[1] = 1
elif predicted_herd[0] == 3:
    herd[2] = 1
elif predicted_herd[0] == 4:
    herd[3] = 1
elif predicted_herd[0] == 5:
    herd[4] = 1

feed_data = np.squeeze(feed_data)
full_input_data = np.hstack((feed_data, microbiome_data, herd)).reshape(1, -1)
full_input_data = preprocess.transform(full_input_data)

st.markdown("""
    <style>
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        width: 100%;
        height: 50px;
        font-size: 18px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.header('Predicted Methane Emissions (g/d)')
col = st.columns([1, 1])
with col[0]:
    if st.button('Predict'):
        if model_option == 'LightGBM':
            predicted_methane = lightgbm_model.predict(full_input_data)
        elif model_option == 'XGBoost':
            predicted_methane = xgboost_model.predict(full_input_data)
        elif model_option == 'SVR':
            predicted_methane = svr_model.predict(full_input_data)
        elif model_option == 'Elastic Net':
            predicted_methane = elastic_model.predict(full_input_data)
        elif model_option == 'MLP':
            input_tensor = torch.FloatTensor(full_input_data)
            predicted_methane = [mlp_model(input_tensor).item()]
        elif model_option == 'KNN':
            predicted_methane = knn_model.predict(full_input_data)
            
        st.write(f'Predicted Methane Emission: {predicted_methane[0]:.2f} g/d')

with col[1]:
    if st.button('Predict all'):
        predicted_methane_mlp = mlp_model(torch.FloatTensor(full_input_data)).item()
        predicted_methane_lightgbm = lightgbm_model.predict(full_input_data)
        predicted_methane_xgboost = xgboost_model.predict(full_input_data)
        predicted_methane_svr = svr_model.predict(full_input_data)
        predicted_methane_elastic = elastic_model.predict(full_input_data)
        predicted_methane_knn = knn_model.predict(full_input_data)
        
        st.write(f'Predicted Methane Emission (MLP): {predicted_methane_mlp:.2f} g/d')
        st.write(f'Predicted Methane Emission (LightGBM): {predicted_methane_lightgbm[0]:.2f} g/d')
        st.write(f'Predicted Methane Emission (XGBoost): {predicted_methane_xgboost[0]:.2f} g/d')
        st.write(f'Predicted Methane Emission (SVR): {predicted_methane_svr[0]:.2f} g/d')
        st.write(f'Predicted Methane Emission (Elastic Net): {predicted_methane_elastic[0]:.2f} g/d')
        st.write(f'Predicted Methane Emission (KNN): {predicted_methane_knn[0]:.2f} g/d')


# To run the app, use the command: streamlit run main.py
