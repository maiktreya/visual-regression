# LOGIC FROM STREAMLIT APP FETCHING DATA FROM SECURED FASTAPI
import requests
import pandas as pd
import streamlit as st
BASE_URL = "http://fastapi-juliani:8000"

# FETCH CLASS AND METHODS


class Fetch():
    # Main method for fetching requested data

    def fetch_data(url: str) -> pd.DataFrame:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # print(data)  # Print the data
            if data:
                df = pd.DataFrame(data)
                return df
        except requests.exceptions.HTTPError as err:
            st.error(f"Error: {err}")
        return pd.DataFrame()

    # Auxiliary methods built over fetch_data

    def fetch_time_serie(equipo: int, pos: int, days: int = 1):
        df = Fetch.fetch_data(
            f"{BASE_URL}/dtimeseries/{equipo}/{int(pos)}?days={days}")
        if not df.empty:
            df['fecha'] = pd.to_datetime(
                df['fecha'], format="%Y-%m-%dT%H:%M:%S.%f", errors='coerce')
        return df

    def fetch_latest_readings(equipo: int) -> pd.DataFrame:
        return Fetch.fetch_data(f"{BASE_URL}/latest_readings/{equipo}")

    def fetch_unique_names(tipo: str) -> pd.DataFrame:
        return Fetch.fetch_data(f"{BASE_URL}/contingency/{tipo}")

    def fetch_metadata() -> pd.DataFrame:
        return Fetch.fetch_data(f"{BASE_URL}/metadata")