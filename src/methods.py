# Functional based methods to use anywhere in the frontend

import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import iirfilter
from datetime import datetime
import statsmodels.api as sm



# start strealit cache to avoid useless reloading
@st.cache_data

# convert a given df to a format suitable to download formatted as spanish delimited csv
def convert_df_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8-sig')

# prepare for unploading csv


def prepare_upload(uploaded_file):
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)

        return (dataframe)

# read from a csv file using spanish/french formatting


def read_file(file):
    # Reading the file with pandas
    df = pd.read_csv(file, delimiter=";", decimal=",")

    return df

# make a link clickable


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split("=")[-2]
    text = text.split("&")[0]

    return f'<a target="_blank" href="{link}">{text}</a>'

# Define the data analysis functions


def jackknife(data, func):
    n = len(data)
    idx = np.arange(n)
    estimates = np.array([func(data[idx != i]) for i in range(n)])
    return estimates

# creates a filter for a FTT analysis of a waveform


def create_notch_filter(frequency, Q, fs):
    nyquist = 0.5 * fs
    freq = frequency / nyquist
    b, a = iirfilter(2, [freq / np.sqrt(Q), freq * np.sqrt(Q)],
                     btype='bandstop', ftype='butter')
    return b, a

# generates a random time series to perform examples


def generate_time_series(n):
    # Generates n random data points
    series_a = np.random.randn(n).cumsum()
    series_b = np.random.randn(n).cumsum()
    # Create a DataFrame
    df = pd.DataFrame({'Series A': series_a, 'Series B': series_b})

    return df

# generate live concurrent timeseries for plotted dynamic charts
def generate_df(selected_data, equipo, days):
    df_all = pd.DataFrame()
    for data in selected_data:
        ts = fetch_time_serie(equipo, data["pos"], days)
        ts.set_index("fecha", inplace=True)
        ts.rename(
            columns={"val": f'{data["pos"]} - {data["nam"]}'}, inplace=True)
        if df_all.empty:
            df_all = ts
        else:
            df_all = df_all.join(ts, how="outer")
    return df_all


## get cummulative distribution function

def cumdis(data):
    x = np.sort(data)

    #calculate CDF values
    y = 1. * np.arange(len(data)) / (len(data) - 1)

    #plot CDF
    z = pd.DataFrame(y, x)
    return z


def translate_summary(results):
    summary = results.summary().tables[1].as_text()

    translations = {
    'Dep. Variable': 'Variable Dep.',
    'R-squared': 'R-cuadrado',
    'Model': 'Modelo',
    'Adj. R-squared': 'R-cuadrado ajustado',
    'Method': 'Método',
    'Least Squares': 'Mínimos Cuadrados',
    'F-statistic': 'Estadística F',
    'Date': 'Fecha',
    'Prob (F-statistic)': 'Prob (Estadística F)',
    'Time': 'Hora',
    'Log-Likelihood': 'Log-verosimilitud',
    'No. Observations': 'No. Observaciones',
    'AIC': 'AIC',
    'Df Residuals': 'Df Residuales',
    'BIC': 'BIC',
    'Df Model': 'Df Modelo',
    'Covariance Type': 'Tipo de Covarianza',
    'nonrobust': 'no robusta',
    'coef': 'coef',
    'std err': 'error estándar',
    'P>|t|': 'P>|t|',
    'Omnibus': 'Omnibus',
    'Durbin-Watson': 'Durbin-Watson',
    'Prob(Omnibus)': 'Prob(Omnibus)',
    'Jarque-Bera (JB)': 'Jarque-Bera (JB)',
    'Skew': 'Asimetría',
    'Prob(JB)': 'Prob(JB)',
    'Kurtosis': 'Curtosis',
    'Cond. No.': 'Cond. No.',
    'Notes:': 'Notas:',
    'Standard Errors assume that the covariance matrix of the errors is correctly specified.': 'Se as'}

    for eng, spa in translations.items():
        summary = summary.replace(eng, spa)

    return summary

# define style CSS/JS overriding streamlit defaults


no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}º
    </style>
"""
sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: block;}
    </style>
"""
