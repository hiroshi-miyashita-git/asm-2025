FROM python:3.12
RUN  apt-get update && apt-get -y install vim \
 &&  pip3 install streamlit google-genai
 
