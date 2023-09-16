# QAG-Streamlit

Build a streamlit application with Docker concerning "Questions au gouvernement (QAG)" at the Assemblée Nationale.

## Application

The application consists in descriptive statistics on QAG sessions under the XVth Assemblée Nationale legislature and in a friendly interface to dig into the content of the QAG.

## Data

The data used by the application can be downloaded directly on the Assemblée Nationale related website:

- The QAG data: https://data.assemblee-nationale.fr/archives-xve/questions-au-gouvernement
- To get the deputies names: https://data.assemblee-nationale.fr/archives-xve/deputes-senateurs-et-ministres
  Last checked: 09/16/2023.

## How to run the application ?

First of all, download the repository.
Then download the data above and place the corresponding folders directly in the folder of this repository.
Make sure the repo is named "qag_streamlit" and the data folders are named "json_qag" and "json_deputes".

Once this is done, running the application is simple with the use of Docker:

- Build the Docker image of the application with the Dockerfile of the repo ;
- Run a container of this application.

If you have problems doing so, feel free to check this tutorial:
https://docs.docker.com/get-started/

## Architecture

This application was built with the library streamlit.
There are two .py files:

- qag_preprocess.py is used to (pre)process the data ;
- qag_streamlit.py is used to build the streamlit application from the processed data.

## TODO:

- Group ministries that are related (all the different Transition Ecologique for example)
