# TO BUILD RUN: "docker build -t streamlit ."" (cd previously to the image own folder containing this dockerfile)
# TO RUN USE: "docker run --name streamlit-juliani -p 8501:8501 -d streamlit"
#-----------------------------------------------------------------------
# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements_streamlit.txt file into the container
COPY requirements_streamlit.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements_streamlit.txt

# Expose the port for Streamlit
EXPOSE 8501

# Start the Streamlit application
CMD streamlit run main.py
