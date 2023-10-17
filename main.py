import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import statsmodels.api as sm
from src.methods import read_file, generate_time_series, cumdis

st.set_page_config(layout="wide")

# Initialize empty DataFrame
df = pd.DataFrame()

# Title of the Streamlit app
st.subheader('Regresión lineal: Análisis de sesgo')

# Layout the selection
with st.sidebar:
    option = st.selectbox(
        '¿Preparado para usar tus propios datos?',
        ('Generador aleatorio', 'Upload CSV File'))

    if option == 'Generador aleatorio':
        with st.container():
            # Number of data points
            n = st.number_input('Seleccione número de observaciones',
                                min_value=10, max_value=1000, value=100)

            # Generate data
            df = generate_time_series(n)

    elif option == 'Upload CSV File':
        with st.container():
            # Upload the CSV file
            file = st.file_uploader('Upload your CSV file')

            # Ask for the column names
            column_name_A = st.text_input(
                'Enter the column name for Series A')
            column_name_B = st.text_input(
                'Enter the column name for Series B')

            # Read the data only if the file is uploaded and column names are provided
            if file and column_name_A and column_name_B:
                df = read_file(file)

                # Selecting the columns for analysis
                df = df[[column_name_A, column_name_B]]
                df.columns = ['Series A', 'Series B']

    # Rest of the code for regression and plotting
if not df.empty:

    # Fit the regression model
    X = sm.add_constant(df['Series A'])
    model = sm.OLS(df['Series B'], X)
    results = model.fit()

    # Calculate residuals and create residuals plot
    df['Residuals'] = df['Series B'] - results.fittedvalues
    alpha = results.params['const']
    beta = results.params['Series A']
    res = results.summary()
    
    # Create the Altair chart object
    scatter_plot = alt.Chart(df).mark_circle().encode(
        alt.X('Series A:Q'),
        alt.Y('Series B:Q')
    )
    # Create regression line
    reg_line = pd.DataFrame({
        'Series A': df['Series A'],
        'Predicted Series B': results.fittedvalues
    })
    line_plot = alt.Chart(reg_line).mark_line(color='red').encode(
        alt.X('Series A:Q'),
        alt.Y('Predicted Series B:Q')
    )
    # Print the simplified regression equation with 3 decimals of precision
    st.write("Ecuación de regresión resultado:")
    st.code(str(f'y = {alpha:.3f} + {beta:.3f}*x'))
    # Display the charts in the Streamlit app
    cols1, cols2 = st.columns([3, 2])

    with cols1:
        st.altair_chart(scatter_plot + line_plot, use_container_width=True)
        tab1, tab2 = st.tabs(
            ["Residuos", "Distribución acumulativa (residuos)"])
        with tab1:
            st.write("Residuos")
            st.bar_chart(df['Residuals'], use_container_width=True)
        with tab2:
            st.write("Distribución acumulativa (residuos)")
            st.line_chart(cumdis(df['Residuals']))
    with cols2:
        tab1, tab2 = st.tabs(["Resultados", "Ayuda"])
        with tab1:
            st.write(res)
        with tab2:
            st.write("R^2 (R-Squared): Coeficiente de determinación. Valor entre 0 y 1. Explica el porcentaje de variación sobre el total explicado por la recta de regresión.")
            st.write("Log-likelihood (Verosimilitud): Medida de cuán probable es obtener nuestros datos observados dado nuestro modelo. Valores más altos indican un mejor ajuste del modelo a los datos.")
            st.write("Valor P: Un indicador estadístico que mide la probabilidad de que los resultados de su prueba sean aleatorios (o 'por suerte'). Un valor P pequeño (menor a 0.05) sugiere que los resultados son significativos.")
            st.write("Estadístico t: Un valor que compara el ratio entre un coeficiente y su desv. típica. Cuanto mayor en v.absoluto más significativo. Aprox: t=2 p-value=0.05.")
            st.write("Omnibus: Prueba estadística que evalúa si la distribución de los residuos es normal. Un valor cercano a 1 sugiere una mayor normalidad.")
            st.write("Durbin-Watson: Estadística que detecta la presencia de autocorrelación en los residuos de una regresión. Valores entre 1.5 y 2.5 sugieren que no hay autocorrelación significativa.")
            st.write("Jarque-Bera: Prueba que evalúa si los residuos tienen la asimetría y la curtosis correspondientes a una distribución normal. Valores cercanos a 0 indican normalidad.")
    st.write(np.transpose(df))
