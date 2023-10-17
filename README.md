# visual-regression
A tool build with streamlit/Python to create an easy web-application to perform linear regression and show common analysis statistics in an interactive way.

## build notes
This app has been derived from a general production setup combining docker + compose.

## app funcionality

- Estimates a linear model by Max. Likelihood from either random data or a .csv file provided by the user. The web-app calculates and reports live the following elements (by up-down order of apperance):
    - Reports a simplified equation of regression.
    - Graphs its associated scatterplot (left).
    - Reports main model description/statistics (right).
        - and gives an intuitive collection of tips for their interpretation (second tab).
    - Plots obtained residuals (left). 
        - reports cummulative sum of residuals (second tab).
    - A data.table with overflow shows the three main model series Exogenous Regressor (X), Endogenous Regressor (Y), and regression residuals (ê).
        - there is a button allowing the download of these series.

and plots its associate

## live example
There is an instance of the app described in this repository running on a free server of https://share.streamlit.io/
The app could be accessed through the following link (lasat check 17/10/2023):
---------------------------------------
https://visual-regression.streamlit.app/
---------------------------------------