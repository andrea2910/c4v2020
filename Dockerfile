# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
#FROM python:alpine
FROM jupyter/scipy-notebook
# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=c4v Version=0.0.1
EXPOSE 3000

WORKDIR /app
ADD . /app

# RUN apt-get update \
#   && apt-get install -yq --no-install-recommends \
#     curl \
#     default-libmysqlclient-dev \
#     libmariadbclient18 \
#     libpq-dev \
#     openssh-client \
#   && apt-get autoremove -y 

# Using pip:
RUN python3 -m pip install -r requirements.txt

#RUN jupyter lab --no-browser --port=3000 --allow-root
#CMD ["python3", "-m", "c4v"]

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "c4v"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m c4v"
